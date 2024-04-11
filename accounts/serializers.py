from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['cu_id', 'cu_name', 'cu_phonenumber', 'cu_email', 'cu_location']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields=['cu_name','cu_phonenumber','cu_email','cu_location']

class CustomerRegiserSerializer(serializers.ModelSerializer):
    cu_password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = Customer
        fields = ['cu_name','cu_email','cu_password','cu_phonenumber','cu_location','cu_password2']
        extra_kwargs = {
            'cu_password':{'write_only':True}
        }
    def save(self):
        cu_password = self.validated_data['cu_password']
        cu_password2 = self.validated_data['cu_password2']

        if cu_password != cu_password2:
            raise serializers.ValidationError({"Error":"پسورد یکی نیست"})

        if Customer.objects.filter(cu_email = self.validated_data['cu_email']).exists():
            raise serializers.ValidationError({"Error":"ایمیل شما قبلا ثبت شده است"})

        if Customer.objects.filter(cu_phonenumber = self.validated_data['cu_phonenumber']).exists():
            raise serializers.ValidationError({"Error":"شماره شما قبلا ثبت شده است"})
        #if need space phonenumber = delete
        account = Customer (cu_email = self.validated_data['cu_email'] , cu_name = self.validated_data['cu_name'] , cu_phonenumber = self.validated_data['cu_phonenumber'], username = self.validated_data['cu_phonenumber'],password = self.validated_data['cu_password'])
        account.set_password (cu_password)
        account.save()

        return account

class CustomerLoginSerializer(serializers.Serializer):
    cu_phonenumber = serializers.CharField(max_length=11)
    cu_password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        cu_phonenumber = data.get('cu_phonenumber')
        cu_password = data.get('cu_password')

        # Perform any additional validation if needed
        if not cu_phonenumber:
            raise serializers.ValidationError({"cu_phonenumber": "This field is required."})
        if not cu_password:
            raise serializers.ValidationError({"cu_password": "This field is required."})

        return data