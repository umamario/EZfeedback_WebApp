class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')