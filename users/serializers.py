from rest_framework import serializers

from users.models import User, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['reference', 'account', 'date', 'amount', 'type', 'category']

    def validate(self, data):
        if data['type'] == 'inflow' and data['amount'] < 0:
            raise serializers.ValidationError('Inflow should have only positive amounts')
        if data['type'] == 'outflow' and data['amount'] > 0:
            raise serializers.ValidationError('Outflow should have only negative amounts')
        return data


class UserSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, allow_null=True, required=False)

    def create(self, validated_data):
        if 'transactions' in validated_data:
            transactions_data = validated_data.pop('transactions')
        else:
            transactions_data = []
        user = User.objects.create(**validated_data)
        for transaction in transactions_data:
            Transaction.objects.create(user=user, **transaction)
        return user

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'age', 'transactions']
