from arxiv_dataset_query_utils import *


def test_get_abstracts_vocabulary():
    testpaps = [{'title': 'one one eleven', 'abstract': 'one one eleven'}, {'title': 'THREE', 'abstract': 'three FOUR'}]
    testvoc = get_abstracts_vocabulary( testpaps)
    assert testvoc == {'OOV': 0,
                        'NUM': 1,
                        'ETAL': 2,
                        'START_EQUATION': 3,
                        'END_EQUATION': 4,
                        'eleven': 5,
                        'four': 6,
                        'one': 7,
                        'three': 8}
    

def test_refine_vocabulary():
    testpaps = [{'title': 'one one eleven', 'abstract': 'one one eleven'}, {'title': 'THREE', 'abstract': 'three FOUR'}]
    testvoc = get_abstracts_vocabulary( testpaps)
    rtestvoc = refine_vocabulary(testvoc, testpaps, min_occurrences=1)
    assert rtestvoc == testvoc
    rtestvoc = refine_vocabulary(testvoc, testpaps, min_occurrences=2)
    assert rtestvoc == {'OOV': 0,
                        'NUM': 1,
                        'ETAL': 2,
                        'START_EQUATION': 3,
                        'END_EQUATION': 4,
                        'eleven': 5,
                        'one': 6,
                        'three': 7}
    rtestvoc = refine_vocabulary(testvoc, testpaps, min_occurrences=4)
    assert rtestvoc == {'OOV': 0,
                        'NUM': 1,
                        'ETAL': 2,
                        'START_EQUATION': 3,
                        'END_EQUATION': 4,
                        'one': 5}
    
