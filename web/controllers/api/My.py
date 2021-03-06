import json

from flask import jsonify, request, g

from application import db
from common.libs.Helper import selectFilterObj, getDictFilterField, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.food.Food import Food
from common.models.member.MemberCart import MemberCart
from common.models.member.MemberComments import MemberComments
from web.controllers.api import route_api
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem


@route_api.route("/my/order")
def myOrderList():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values

    status = int(req['status']) if 'status' in req else 0
    query = PayOrder.query.filter_by(member_id=member_info.id)

    # 等待付款状态
    if status == -8:
        query = query.filter(PayOrder.status == -8)
    # 待发货
    elif status == -7:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -7, PayOrder.comment_status == 0)
    # 待确认
    elif status == -6:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -6, PayOrder.comment_status == 0)
    # 待评价
    elif status == -5:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 0)
    # 已完成
    elif status == 1:
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 1)
    else:
        query = query.filter(PayOrder.status == 0)

    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    data_pay_order_list = []
    if pay_order_list:
        pay_order_ids = selectFilterObj(pay_order_list, "id")
        pay_order_item_list = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        food_ids = selectFilterObj(pay_order_item_list, "food_id")
        food_map = getDictFilterField(Food, Food.id, "id", food_ids)
        pay_order_item_map = {}
        if pay_order_item_list:
            for item in pay_order_item_list:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []

                tmp_food_info = food_map[item.food_id]
                pay_order_item_map[item.pay_order_id].append({
                    "id": item.id,
                    "food_id": item.food_id,
                    "quantity": item.quantity,
                    "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
                    "name": tmp_food_info.name,
                })

        for item in pay_order_list:
            tmp_data = {
                "status": item.pay_status,
                "status_desc": item.status_desc,
                "date": item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "order_number": item.order_number,
                "order_sn": item.order_sn,
                "note": item.note,
                "total_price": str(item.total_price),
                "goods_list": pay_order_item_map[item.id]
            }

            data_pay_order_list.append(tmp_data)

    resp['data']['pay_order_list'] = data_pay_order_list

    # cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()
    # data_cart_list = []
    # if cart_list:
    #     food_ids = selectFilterObj(cart_list, "food_id")
    #     food_map = getDictFilterField(Food, Food.id, "id", food_ids)
    #     for item in cart_list:
    #         tmp_food_info = food_map[item.food_id]
    #         tmp_data = {
    #             "id": item.id,
    #             "food_id": item.food_id,
    #             "number": item.quantity,
    #             "name": tmp_food_info.name,
    #             "price": str(tmp_food_info.price),
    #             "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
    #             "active": True
    #         }
    #         data_cart_list.append(tmp_data)
    #
    # resp['data']['list'] = data_cart_list

    return jsonify(resp)


@route_api.route("/my/comment/add", methods=["POST"])
def myCommentAdd():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    score = req['score'] if 'score' in req else 10  # 默认10分
    content = req['content'] if 'content' in req else ''

    pay_order_info = PayOrder.query.filter_by(member_id=member_info.id, order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙，请稍后再试"
        return jsonify(resp)

    if pay_order_info.comment_status:
        resp['code'] = -1
        resp['msg'] = "已评价"
        return jsonify(resp)

    pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).all()
    food_ids = selectFilterObj(pay_order_items, "food_id")

    tmp_food_ids_str = '_'.join(str(s) for s in food_ids if s not in [None])

    model_comment = MemberComments()
    model_comment.member_id = member_info.id
    model_comment.food_ids = "_%s_" % tmp_food_ids_str
    model_comment.pay_order_id = pay_order_info.id
    model_comment.score = score
    model_comment.content = content
    model_comment.created_time = getCurrentDate()
    db.session.add(model_comment)

    pay_order_info.comment_status = 1
    pay_order_info.updated_time = getCurrentDate()
    db.session.add(pay_order_info)
    db.session.commit()

    return jsonify(resp)


@route_api.route("/my/comment/list")
def myCommentList():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    comment_list = MemberComments.query.filter_by(member_id=member_info.id) \
        .order_by(MemberComments.id.desc()).all()
    data_comment_list = []
    if comment_list:
        pay_order_ids = selectFilterObj(comment_list, "pay_order_id")
        pay_order_map = getDictFilterField(PayOrder, PayOrder.id, "id", pay_order_ids)
        for item in comment_list:
            tmp_pay_order_info = pay_order_map[item.pay_order_id]
            tmp_data = {
                "date": item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "content": item.content,
                "order_number": tmp_pay_order_info.order_number
            }
            data_comment_list.append(tmp_data)
    resp['data']['list'] = data_comment_list
    return jsonify(resp)
