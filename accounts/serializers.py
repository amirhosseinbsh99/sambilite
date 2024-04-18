from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['cu_name', 'Username', 'cu_email', 'cu_location']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields=['cu_name','username','cu_location','password']

class CustomerRegiserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = Customer
        fields = ['cu_name','cu_email','password','username','cu_location','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"Error":"پسورد یکی نیست"})

        if Customer.objects.filter(cu_email = self.validated_data['cu_email']).exists():
            raise serializers.ValidationError({"Error":"ایمیل شما قبلا ثبت شده است"})

        if Customer.objects.filter(username = self.validated_data['username']).exists():
            raise serializers.ValidationError({"Error":"شماره شما قبلا ثبت شده است"})
        else:

            try:
                token2 = random.randint(10000, 99999)


                api = KavenegarAPI('7937386A425358714D3072664F59414B4D79416D6E444C534C55357A724E33395258437661466F34727A343D')
                phone=Customer.username

                params = {
                'token': token2,
                'receptor':'',
                'template': 'fayateachh',
                    'type': 'sms'
                }
                response = api.verify_lookup(params)
                print(response)
            except APIException as e: 
                print(e)
            except HTTPException as e: 
                print(e)

                account = account.objects.create_user(username=Customer.username,token_send=token2)
                return redirect('accounts:kave_negar_token_send')

    def kave_negar_token_send(self):

        sms_code = self.validated_data['sms_code']
        if Customer.objects.filter(token_send=sms_code).exists():
            Customer.objects.filter(token_send=sms_code).delete()

            account = Customer (cu_email = self.validated_data['cu_email'] , cu_name = self.validated_data['cu_name'] , username = self.validated_data['username'], password = self.validated_data['password'])
            account.set_password (password)
            account.save()

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=11)
    password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Perform any additional validation if needed
        if not username:
            raise serializers.ValidationError({"username": "This field is required."})
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        return data
    
    