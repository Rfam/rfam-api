"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from api.models import Genome, Family, Rfamseq, FullRegion, Taxonomy
from rest_framework import routers, serializers, viewsets, generics

# Serializers define the API representation.
class GenomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genome
        fields = '__all__'

# ViewSets define the view behavior.
class GenomeViewSet(viewsets.ModelViewSet):
    queryset = Genome.objects.all()
    serializer_class = GenomeSerializer

class FamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class RfamseqSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rfamseq
        fields = ('description', 'ncbi_id', 'rfamseq_acc', 'length')
        depth = 1

class RfamseqViewSet(viewsets.ModelViewSet):
    queryset = Rfamseq.objects.all()
    serializer_class = RfamseqSerializer

class TaxonomySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'

class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer

class FullRegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FullRegion
        fields = ( 'bit_score', 'cm_end', 'cm_start', 'evalue_score', 'is_significant',
        'rfam_acc', 'seq_end', 'seq_start', 'truncated')
        depth = 1

class FullRegionDetailView(generics.ListAPIView):
    """
    View details about Rfam hits.
    Optionally filter using "start" and "end" URL query parameters.
    """
    serializer_class = FullRegionSerializer

    def get_queryset(self):
        rfamseq_acc = self.kwargs['rfamseq_acc']
        queryset = FullRegion.objects.filter(rfamseq_acc=rfamseq_acc).all()
        seq_start = self.request.query_params.get('start', None)
        seq_end = self.request.query_params.get('end', None)
        if seq_start and seq_end:
            queryset = queryset.filter(seq_start=seq_start, seq_end=seq_end)
        return queryset

class FullRegionViewSet(viewsets.ModelViewSet):
    queryset = FullRegion.objects.all()
    serializer_class = FullRegionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'genomes', GenomeViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'rfamseq', RfamseqViewSet)
router.register(r'taxonomy', TaxonomyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^full_region/(?P<rfamseq_acc>.+)/$', FullRegionDetailView.as_view()),
]
