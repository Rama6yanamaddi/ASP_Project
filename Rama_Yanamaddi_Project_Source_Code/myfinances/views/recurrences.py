from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from myfinances.forms import DepositForm, RecurringTransactionForm, TransferForm, WithdrawForm
from myfinances.lib import last_day_of_month
from myfinances.models import RecurringTransaction, Transaction


class RecurrenceCreateView(LoginRequiredMixin, generic.edit.CreateView):
    form_class = RecurringTransactionForm
    model = RecurringTransaction
    success_url = reverse_lazy('recurrences')


class ReccurrenceSetNextOccurence(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        for r in RecurringTransaction.objects.due_in_month():
            old = r.date
            t = r.recurrences.first()
            if not t:
                continue
            while t.date >= r.date:
                r.date = r.update_date()
            if old != r.date:
                r.save()
        return HttpResponseRedirect(reverse('recurrences'))


class RecurrenceDetailView(LoginRequiredMixin, generic.DetailView):
    model = RecurringTransaction
    context_object_name = 'recurrence'


class RecurrenceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    form_class = RecurringTransactionForm
    model = RecurringTransaction
    success_url = reverse_lazy('recurrences')


class RecurrenceTransactionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Transaction
    template_name = 'myfinances/transaction_edit.html'

    def get_form(self, form_class=None):
        self.recurrence = get_object_or_404(RecurringTransaction, pk=self.kwargs['pk'])
        if self.recurrence.transaction_type == Transaction.WITHDRAW:
            form_class = WithdrawForm
        elif self.recurrence.transaction_type == Transaction.DEPOSIT:
            form_class = DepositForm
        else:
            form_class = TransferForm
        return form_class(**self.get_form_kwargs())

    def get_initial(self):
        initial = super().get_initial()
        initial['title'] = self.recurrence.title
        initial['source_account'] = self.recurrence.src
        initial['destination_account'] = self.recurrence.dst
        initial['amount'] = self.recurrence.amount
        initial['date'] = self.recurrence.date
        initial['recurrence'] = self.recurrence.pk
        initial['category'] = self.recurrence.category
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.recurrence = self.recurrence
        self.object.save()
        self.recurrence.update_date(save=True)
        return response


class RecurrenceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = RecurringTransaction
    success_url = reverse_lazy('recurrences')


class RecurringTransactionIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'myfinances/recurring_transactions.html'
    context_object_name = 'transactions'
    queryset = RecurringTransaction.objects.exclude(interval=RecurringTransaction.DISABLED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = 'recurrences'
        income = 0
        expenses = 0
        today = date.today()
        last = last_day_of_month(today)
        remaining = 0
        for t in context['transactions']:
            if t.interval == RecurringTransaction.MONTHLY or (
                    t.interval == RecurringTransaction.ANNUALLY and
                    t.date.month == today.month and t.date.year == today.year):
                if t.transaction_type == Transaction.WITHDRAW:
                    expenses += t.amount
                    if t.date <= last:
                        remaining -= t.amount
                elif t.transaction_type == Transaction.DEPOSIT:
                    income += t.amount
                    if t.date <= last:
                        remaining += t.amount
        context['expenses'] = expenses
        context['income'] = income
        context['total'] = income - expenses
        context['remaining'] = remaining
        return context


class DisabledRecurrencesView(LoginRequiredMixin, generic.ListView):
    template_name = 'myfinances/disabled_recurrences.html'
    queryset = RecurringTransaction.objects.filter(interval=RecurringTransaction.DISABLED)
    paginate_by = 20
