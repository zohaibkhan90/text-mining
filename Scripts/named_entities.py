import nltk
import event_detection as ts

x, y = ts.pre()

namedEntities = set()

def extractNE(tree):
    namedEntity = ''
    for leafNode in tree.leaves():
        namedEntity += leafNode[0] + ' '
    return namedEntity.strip()

def process_content():
    try:
        for i in x:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            namedEnt = nltk.ne_chunk(tagged, binary=True)
            
            for subtree in namedEnt.subtrees():
                s = subtree.label()
                if s == 'NE':
                    namedEntity = extractNE(subtree)
                    namedEntities.add(namedEntity)
                    
    except Exception as e:
        print(str(e))
process_content()

print(namedEntities)