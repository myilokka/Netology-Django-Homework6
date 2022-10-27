from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['price', 'quantity', 'product']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions_data:
            product = position.get('product')
            price = position.get('price')
            quantity = position.get('quantity')
            StockProduct.objects.create(stock=stock, product=product, price=price, quantity=quantity)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for position in positions:
            price = position.get('price')
            quantity = position.get('quantity')
            product = position.get('product')
        pos, created = StockProduct.objects.update_or_create(price=price, quantity=quantity, defaults={'product': product,'stock': stock})

        return stock

