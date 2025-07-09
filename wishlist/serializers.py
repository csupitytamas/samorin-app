from rest_framework import serializers
from .models import Wishlist, WishlistPoleItem, WishlistWingItem
from warehouse.models import Pole, Wings

class WishlistPoleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistPoleItem
        fields = ['id', 'pole', 'quantity']

class WishlistWingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistWingItem
        fields = ['id', 'wing', 'quantity']

class WishlistSerializer(serializers.ModelSerializer):
    pole_items = WishlistPoleItemSerializer(many=True)
    wing_items = WishlistWingItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'created_by', 'arena', 'created_at', 'note', 'pole_items', 'wing_items']

    def create(self, validated_data):
        pole_items_data = validated_data.pop('pole_items', [])
        wing_items_data = validated_data.pop('wing_items', [])
        wishlist = Wishlist.objects.create(**validated_data)

        for item_data in pole_items_data:
            WishlistPoleItem.objects.create(wishlist=wishlist, **item_data)
        for item_data in wing_items_data:
            WishlistWingItem.objects.create(wishlist=wishlist, **item_data)
        return wishlist