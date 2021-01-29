from antismash_models import SyncJob as Job

b = Job("a", "123")
#b.taxon = True

print(b.all_orfs)