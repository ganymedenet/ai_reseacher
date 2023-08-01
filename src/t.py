from core.data.industries import Industries
from core.data.tagger import Tagger


# ind = Industries()

#print(ind.list)
tg = Tagger()

tags = "#Apple, #iPhone, #ArtificialIntelligence"

res = tg.validate_tags(tags)
