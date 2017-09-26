
# import os
import provenance_indexedContents as provenance_indexedContents
db=provenance_indexedContents.ProvenanceStore("mongodb://127.0.0.1/verce-prov")


print 'start'
db.insert();
print 'end'

