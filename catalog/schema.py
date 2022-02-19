import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import Category, Product


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.Node, )
        filter_fields = ('name', )


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = ('name', 'price')


class Query:
    all_categories = DjangoFilterConnectionField(CategoryType)
    all_products = graphene.List(ProductType)
    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    product = graphene.Field(ProductType, id=graphene.Int(), name=graphene.String())

    # def resolve_all_categories(self, info, **kwargs):
    #     return Category.objects.all()

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.select_related('category').all()

    def resolve_category(self, info, **kwargs):
        if 'id' in kwargs:
            return Category.objects.get(id=kwargs['id'])
        elif 'name' in kwargs:
            return Category.objects.get(name=kwargs['name'])
        else:
            return None

    def resolve_product(self, info, **kwargs):
        if 'id' in kwargs:
            return Product.objects.get(id=kwargs['id'])
        elif 'name' in kwargs:
            return Product.objects.get(name=kwargs['name'])
        else:
            return None
