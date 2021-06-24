from rest_framework import serializers

class PlannerSearchSerializer(serializers.Serializer):
    q = serializers.CharField(default='')
    period = serializers.RegexField(r'\d{4}-\d', required=True)
    campus = serializers.ListField(child=serializers.CharField(), default=[])
    format = serializers.ListField(child=serializers.CharField(), default=[])
    school = serializers.ListField(child=serializers.CharField(), default=[])
    mod_types = serializers.ListField(child=serializers.CharField(), default=[])
    area = serializers.ListField(child=serializers.CharField(), default=[])
    category = serializers.ListField(child=serializers.CharField(), default=[])
    overlap = serializers.BooleanField()
    overlap_except = serializers.BooleanField()
    schedule = serializers.CharField(default='')
    max_mod = serializers.IntegerField(min_value=0, default=None)
    credits = serializers.IntegerField(min_value=0, default=None)
    without_req = serializers.BooleanField()
    free_quota = serializers.BooleanField()

    page = serializers.IntegerField(min_value=1, default=1)
