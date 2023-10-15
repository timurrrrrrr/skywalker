from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Category, Product, CartItem
from .serializers import CustomUserSerializer, ProductSerializer, CategorySerializer, CartItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                'access_token': access_token,
                'message': 'User registered successfully.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=serializer.validated_data['product'].pk)
        serializer.save(user=self.request.user)

        existing_cart_item = CartItem.objects.filter(user=self.request.user, product=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += serializer.validated_data['quantity']
            existing_cart_item.save()
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({'message': 'Product added to cart successfully'})


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    paginate_by = 10

    def get_queryset(self):
        category = self.request.query_params.get('category')

        if category:
            return Product.objects.filter(category=category)
        return Product.objects.all()


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
        return Product.objects.all()
