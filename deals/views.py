import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count, Case, When, IntegerField
from django.http import HttpResponse, request
from .models import Deal
from .forms import DealForm, ReportForm


class DealListView(LoginRequiredMixin, ListView):
    model = Deal
    template_name = "deal_list.html"  # Remove 'deals/' prefix
    context_object_name = "deals"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(stock_number__icontains=query)
                | Q(deal_date__icontains=query)
                | Q(last_name__icontains=query)
            )
        return queryset


class DealCreateView(LoginRequiredMixin,CreateView):
    model = Deal
    form_class = DealForm
    template_name = "deal_form.html"  # Remove 'deals/' prefix
    success_url = reverse_lazy("deal-list")


class DealUpdateView(LoginRequiredMixin,UpdateView):
    model = Deal
    form_class = DealForm
    template_name = "deal_form.html"  # Remove 'deals/' prefix
    success_url = reverse_lazy("deal-list")


class DealDeleteView(LoginRequiredMixin,DeleteView):
    model = Deal
    template_name = "deal_confirm_delete.html"  # Remove 'deals/' prefix
    success_url = reverse_lazy("deal-list")


class ReportView(LoginRequiredMixin,FormView):
    template_name = "report.html"
    form_class = ReportForm

    def form_valid(self, form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        managers = form.cleaned_data["managers"]

        deals = Deal.objects.all()

        if start_date:
            deals = deals.filter(deal_date__gte=start_date)
        if end_date:
            deals = deals.filter(deal_date__lte=end_date)
        if managers:
            deals = deals.filter(manager__in=managers)

        profit_sum = deals.aggregate(
            total_profit=Sum("reserve")
            + Sum("vsc")
            + Sum("gap")
            + Sum("tw")
            + Sum("tricare")
            + Sum("key")
        )
        total_profit = profit_sum["total_profit"] or 0
        total_deals = deals.count()
        avg_profit_per_car = total_profit / total_deals if total_deals > 0 else 0

        products_sold = deals.aggregate(
            vsc_sold=Count(Case(When(vsc__gt=0, then=1), output_field=IntegerField())),
            gap_sold=Count(Case(When(gap__gt=0, then=1), output_field=IntegerField())),
            tw_sold=Count(Case(When(tw__gt=0, then=1), output_field=IntegerField())),
            tricare_sold=Count(
                Case(When(tricare__gt=0, then=1), output_field=IntegerField())
            ),
            key_sold=Count(Case(When(key__gt=0, then=1), output_field=IntegerField())),
        )

        avg_products_sold = (
            sum(products_sold.values()) / total_deals if total_deals > 0 else 0
        )

        context = self.get_context_data(form=form)
        context.update(
            {
                "total_profit": total_profit,
                "total_deals": total_deals,
                "avg_profit_per_car": avg_profit_per_car,
                "avg_products_sold": avg_products_sold,
                "products_sold": products_sold,
            }
        )

        if "export_csv" in self.request.POST:
            return self.export_csv(deals, context)

        return self.render_to_response(context)

    def export_csv(self, deals, context):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="deals_report.csv"'

        writer = csv.writer(response)

        # Get all field names from the Deal model
        fields = [field.name for field in Deal._meta.fields]

        # Write header row
        writer.writerow(fields)

        # Write data rows
        for deal in deals:
            writer.writerow([getattr(deal, field) for field in fields])

        return response
