from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Category, Product, Brand, CartItem
from .serializers import CustomUserSerializer, BrandSerializer, ProductSerializer, CategorySerializer
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


class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class AddToCartView(CreateView):
    model = CartItem
    fields = ['product', 'quantity']

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=form.instance.product.pk)
        form.instance.user = self.request.user
        existing_cart_item = CartItem.objects.filter(user=self.request.user, product=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += form.instance.quantity
            existing_cart_item.save()
        else:
            form.save()

        return JsonResponse({'message': 'Product added to cart successfully'})

    def form_invalid(self, form):
        return JsonResponse({'message': 'Failed to add product to cart'})


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category = self.request.GET.get('category')

        if category:
            return Product.objects.filter(category=category)
        else:
            return Product.objects.all()


class ProductSearchView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
        return Product.objects.all()
