from arxiv_dataset_iterator import gather_iterator


def test_gather_iterator():
    ids_of_interest = ['id0', 'id1', 'id2', 'id3', 'id4', 'id5', 'id6', 'id7', 'id8', 'id9',
                       'id10', 'id11', 'id12', 'id13', 'id14', 'id15', 'id16', 'id17', 'id18', 'id19']
    dir_origin = 'arXiv_dataset_iterator_test_files'
    dir_destin = 'arXiv_destin'

    kwargs = {'start_index': 3,
              'end_index': 16,
              'dir_size': 10,
              'use_dirs': True,
              'make_dirs': False, # do not change this, will check for and create dirs
              'break_bool': True, # should not even be checked
              'exist_ok': False, # to be safe - should not even be checked
              'verbose': False,
              'print_every': None}

    ids_passed = []
    for i, args_dict in enumerate(gather_iterator(ids_of_interest, dir_origin, dir_destin, **kwargs), start=kwargs['start_index']):
        assert args_dict['ind'] == i # index in ids of interest
        assert args_dict['id'] == f'id{i}'
        ids_passed.append(args_dict['id'])
        if i < 10:
            assert args_dict['file_origin'] == f"{dir_origin}/0-9__id0__to__id9/{i}__id{i}.json"
            assert args_dict['file_destin'] == f"{dir_destin}/0-9__id0__to__id9/{i}__id{i}.json"
        else:
            assert args_dict['file_origin'] == f"{dir_origin}/10-19__id10__to__id19/{i}__id{i}.json"
            assert args_dict['file_destin'] == f"{dir_destin}/10-19__id10__to__id19/{i}__id{i}.json"
        assert args_dict['gather'] == {f'id{i}': {'file1': [{'e': 'equation', 'l': 1, 't': 'b'}]}}

    assert ids_passed == ['id3', 'id4', 'id5', 'id6', 'id7', 'id8', 'id9', 'id10', 'id11', 'id12', 'id13', 'id14', 'id15', 'id16']



# import os
# def create_test_directory():
#     os.makedirs("arXiv_dataset_iterator_test_files/0-99__id0__to__id99", exist_ok=True)
#     for i in range(0, 100):
#         with open(f"arXiv_dataset_iterator_test_files/0-99__id0__to__id99/{i}__id{i}.json", "w") as f:
#             gather = {f'id{i}': {'file1': [{'e': 'equation', 'l': 1, 't': 'b'}]}}
#             json.dump(gather, f)
