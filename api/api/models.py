"""
Copyright [2009-2017] EMBL-European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.db import models


class Genome(models.Model):
    upid = models.CharField(max_length=20, primary_key=True)
    ncbi_id = models.IntegerField(db_index=True)
    description = models.TextField()
    length = models.IntegerField(db_column='total_length')
    scientific_name = models.CharField(max_length=300)
    common_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'genome'


class Family(models.Model):
    rfam_acc = models.CharField(max_length=7, primary_key=True)
    rfam_id = models.CharField(max_length=40, db_index=True)
    description = models.CharField(max_length=75)
    type = models.CharField(max_length=50, db_index=True)
    num_seed = models.IntegerField()
    num_full = models.IntegerField()
    number_of_species = models.IntegerField()
    author = models.TextField()

    class Meta:
        db_table = 'family'


class Rfamseq(models.Model):
    rfamseq_acc = models.CharField(max_length=20, primary_key=True)
    accession = models.CharField(max_length=15)
    version = models.IntegerField()
    ncbi_id = models.ForeignKey('Taxonomy', to_field='ncbi_id', db_column='ncbi_id')
    length = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'rfamseq'


class FullRegion(models.Model):
    id = models.AutoField(primary_key=True)
    rfam_acc = models.ForeignKey('Family', to_field='rfam_acc', db_column='rfam_acc')
    rfamseq_acc = models.ForeignKey('Rfamseq', to_field='rfamseq_acc', db_column='rfamseq_acc')
    seq_start = models.IntegerField()
    seq_end = models.IntegerField()
    bit_score = models.FloatField()
    evalue_score = models.FloatField()
    cm_start = models.IntegerField()
    cm_end = models.IntegerField()
    truncated = models.CharField(max_length=1)
    type = models.CharField(max_length=4, db_index=True)
    is_significant = models.IntegerField(db_index=True)

    class Meta:
        db_table = 'full_region'


class Taxonomy(models.Model):
    ncbi_id = models.IntegerField(primary_key=True)
    species = models.CharField(max_length=100)
    tax_string = models.TextField()

    class Meta:
        db_table = 'taxonomy'
