from pf_sqlalchemy.crud.pfs_rest_helper_service import pfs_crud


def get_ids_and_view_order_list(listOfModelViewSort: list):
    ids = []
    order = []
    ids_order_dict = {}
    for item in listOfModelViewSort:
        if "id" in item and "viewOrder":
            ids.append(item['id'])
            order.append(item['viewOrder'])
            ids_order_dict[item["id"]] = item['viewOrder']
    return {"ids": ids, "order": order, "ids_order_dict": ids_order_dict}


def update_model_view_sort_order(model, ids_order_param):
    try:
        id_order_list = get_ids_and_view_order_list(ids_order_param)
        fields = model.query.filter(model.id.in_(id_order_list['ids'])).all()
        ids_order_dict = id_order_list["ids_order_dict"]
        models = []
        for field in fields:
            if field.id in ids_order_dict:
                field.viewOrder = ids_order_dict[field.id]
                models.append(field)
        if models:
            pfs_crud.save_all(models)
    except Exception as e:
        return False
    return True
