import decimal
from collections import defaultdict

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User, Transaction
from users.serializers import UserSerializer, TransactionSerializer


class TransactionViewSet(APIView):
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        transactions = TransactionSerializer(request.data, many=True).data
        for transaction in transactions:
            Transaction.objects.create(user=user, **transaction)
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)


class UserViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserSummaryView(APIView):
    def post(self, request, pk):
        date_start = request.data.get('date_start', None)
        date_end = request.data.get('date_end', None)
        if date_start is not None and date_end is not None:
            transactions = Transaction.objects.filter(user__id=pk, date__gte=date_start, date__lte=date_end)
        else:
            transactions = Transaction.objects.filter(user__id=pk)

        accounts_summary = self.get_account_summary(transactions)
        return Response(accounts_summary)

    def get_account_summary(self, transactions):
        accounts_data = defaultdict(list)
        for t in transactions:
            accounts_data[t.account].append(t)

        return map(self.get_transactions_summary, accounts_data.values())

    def get_transactions_summary(self, transactions):
        balance = inflows = outflows = 0
        for transaction in transactions:
            balance += transaction.amount
            inflows += transaction.amount if transaction.type == 'inflow' else 0
            outflows += transaction.amount if transaction.type == 'outflow' else 0
        return {
            'account': transactions[0].account,
            'balance': balance,
            'total_inflow': inflows,
            'total_outflow': outflows
        }


class UserSummaryPerCategoryView(APIView):
    def get(self, request, pk):
        transactions = Transaction.objects.filter(user__id=pk)
        summary_per_category = self.get_summary_per_category(transactions)
        return Response(summary_per_category)

    def get_summary_per_category(self, transactions):
        inflow_category_dict = defaultdict(decimal.Decimal)
        outflow_category_dict = defaultdict(decimal.Decimal)
        categories_data = defaultdict(list)
        for t in transactions:
            categories_data[t.category].append(t)

        for category_data in categories_data.values():
            for transaction in category_data:
                if transaction.type == 'inflow':
                    inflow_category_dict[transaction.category] += transaction.amount
                elif transaction.type == 'outflow':
                    outflow_category_dict[transaction.category] += transaction.amount
        return {
            "inflow": inflow_category_dict,
            "outflow": outflow_category_dict
        }
