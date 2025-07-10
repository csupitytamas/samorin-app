from rest_framework import serializers
from .models import Wishlist, WishlistPoleItem, WishlistWingItem
from warehouse.models import Pole, Wings

class WishlistPoleItemSerializer(serializers.ModelSerializer):
    pole_name_en = serializers.CharField(source='pole.name_en', read_only=True)
    pole_name_hu = serializers.CharField(source='pole.name_hu', read_only=True)
    pole_color = serializers.CharField(source='pole.color', read_only=True)
    pole_length = serializers.FloatField(source='pole.length', read_only=True)
    class Meta:
        model = WishlistPoleItem
        fields = ['id', 'pole', 'quantity', 'pole_name_en', 'pole_name_hu', 'pole_color', 'pole_length']

class WishlistWingItemSerializer(serializers.ModelSerializer):
    wing_name_en = serializers.CharField(source='wing.name_en', read_only=True)
    wing_name_hu = serializers.CharField(source='wing.name_hu', read_only=True)
    wing_color = serializers.CharField(source='wing.color', read_only=True)

    class Meta:
        model = WishlistWingItem  # Ezt javítani kellett, nem WishlistPoleItem
        fields = ['id', 'wing', 'quantity', 'wing_name_en', 'wing_name_hu', 'wing_color']

class WishlistSerializer(serializers.ModelSerializer):
    pole_items = WishlistPoleItemSerializer(many=True, read_only=True)
    wing_items = WishlistWingItemSerializer(many=True, read_only=True)
    arena_name = serializers.CharField(source='arena.name', read_only=True)
    created_by = serializers.SerializerMethodField()


    # Ezek csak íráskor legyenek, olvasásnál NEM!
    pole_items_input = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    wing_items_input = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Wishlist
        fields = [
            'id', 'created_at', 'arena', 'arena_name', 'created_by',
            'pole_items', 'wing_items', 'pole_items_input', 'wing_items_input', 'note'
        ]
        read_only_fields = ['created_at', 'arena_name', 'created_by', 'pole_items', 'wing_items']

    def create(self, validated_data):
        pole_items_data = validated_data.pop('pole_items_input', [])
        wing_items_data = validated_data.pop('wing_items_input', [])
        wishlist = Wishlist.objects.create(**validated_data)
        for item in pole_items_data:
            pole_instance = Pole.objects.get(pk=item['pole'])
            WishlistPoleItem.objects.create(wishlist=wishlist, pole=pole_instance, quantity=item['quantity'])
        for item in wing_items_data:
            wing_instance = Wings.objects.get(pk=item['wing'])
            WishlistWingItem.objects.create(wishlist=wishlist, wing=wing_instance, quantity=item['quantity'])
        return wishlist

    def update(self, instance, validated_data):
        pole_items_data = validated_data.pop('pole_items_input', [])
        wing_items_data = validated_data.pop('wing_items_input', [])
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        # Régi rekordok törlése
        instance.pole_items.all().delete()
        instance.wing_items.all().delete()
        # Újak mentése
        from warehouse.models import Pole, Wings
        for item in pole_items_data:
            pole_instance = Pole.objects.get(pk=item['pole'])
            WishlistPoleItem.objects.create(wishlist=instance, pole=pole_instance, quantity=item['quantity'])
        for item in wing_items_data:
            wing_instance = Wings.objects.get(pk=item['wing'])
            WishlistWingItem.objects.create(wishlist=instance, wing=wing_instance, quantity=item['quantity'])
        return instance

    def get_created_by(self, obj):
        # Ez lesz a user neve vagy felhasználóneve
        if obj.created_by:
            return getattr(obj.created_by, 'username', None) or str(obj.created_by)
        return None