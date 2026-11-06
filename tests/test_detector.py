from pseudo_tool.detector import Detector


def test_phone_normal():
    d = Detector()
    hits = d.detect("联系 13800001234")
    assert any(h.text == "13800001234" and h.type == "PHONE" for h in hits)


def test_phone_boundary():
    d = Detector()
    hits = d.detect("a13800001234b")
    assert not any(h.type == "PHONE" for h in hits)


def test_dedup():
    d = Detector()
    hits = d.detect("13800001234 13800001234")
    phones = [h for h in hits if h.type == "PHONE"]
    assert len(phones) == 1


def test_email():
    d = Detector()
    hits = d.detect("mail user@example.com")
    assert any(h.type == "EMAIL" for h in hits)


def test_id_card():
    d = Detector()
    hits = d.detect("110101199001011234 11010119900101123X")
    ids = [h for h in hits if h.type == "ID"]
    assert len(ids) >= 1

def test_name_detect():
    d = Detector()
    hits = d.detect("张三和李四签订合同，联系13800001234")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "张三" in names
    assert "李四" in names
    assert "13800001234" not in names

def test_name_hanlp():
    d = Detector()
    hits = d.detect("覃晓明与冼丽华签订合同")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "覃晓明" in names
    assert "冼丽华" in names


def test_name_not_location():
    d = Detector()
    hits = d.detect("北京市朝阳区张三")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "张三" in names
    assert "北京市朝阳区" not in names

def test_address():
    d = Detector()
    hits = d.detect("上海市浦东新区张江路88号")
    addrs = {h.text for h in hits if h.type == "ADDRESS"}
    assert any("张江路88号" in a or a == "上海市浦东新区张江路88号" for a in addrs)


def test_org():
    d = Detector()
    hits = d.detect("北京智源人工智能研究院有限公司")
    orgs = {h.text for h in hits if h.type == "ORG"}
    assert any("智源人工智能研究院有限公司" in o or o == "北京智源人工智能研究院有限公司" for o in orgs)


def test_overlap():
    d = Detector()
    hits = d.detect("张三在阿里巴巴科技有限公司工作，住在杭州市西湖区文三路100号")
    names = {h.text for h in hits if h.type == "NAME"}
    orgs = {h.text for h in hits if h.type == "ORG"}
    addrs = {h.text for h in hits if h.type == "ADDRESS"}
    assert "张三" in names
    assert any("阿里巴巴" in o or "科技有限公司" in o for o in orgs)
    assert any("文三路" in a for a in addrs)

def test_name_rare_surname():
    d = Detector()
    hits = d.detect("覃晓明与冼丽华签订合同")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "覃晓明" in names
    assert "冼丽华" in names


def test_name_compound_surname():
    d = Detector()
    hits = d.detect("欧阳娜娜和司马光开会")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "欧阳娜娜" in names
    assert "司马光" in names


def test_name_not_org():
    d = Detector()
    hits = d.detect("张三在阿里巴巴科技有限公司工作")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "张三" in names


def test_name_tail_check():
    d = Detector()
    hits = d.detect("王伟和赵四")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "王伟" in names
    assert "赵四" in names

def test_name_not_bank_branch():
    d = Detector()
    hits = d.detect("中国工商银行上海张江支行")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "张江" not in names


def test_name_not_road():
    d = Detector()
    hits = d.detect("中关村东路88号")
    names = {h.text for h in hits if h.type == "NAME"}
    assert "东路" not in names
    assert "中关村东路" not in names

def test_uscc():
    d = Detector()
    hits = d.detect("91110108MA01ABCD2X")
    usccs = {h.text for h in hits if h.type == "USCC"}
    assert "91110108MA01ABCD2X" in usccs


def test_no_overlap():
    d = Detector()
    hits = d.detect("张三在阿里巴巴科技有限公司工作，住杭州市西湖区文三路100号")
    names = {h.text for h in hits if h.type == "NAME"}
    orgs = {h.text for h in hits if h.type == "ORG"}
    addrs = {h.text for h in hits if h.type == "ADDRESS"}
    assert "张三" in names
    assert any("阿里" in o or "科技有限公司" in o for o in orgs)
    assert any("文三路" in a for a in addrs)

def test_org_isolated():
    d = Detector()
    hits = d.detect("甲方：北京智源人工智能研究院有限公司，乙方：上海云帆数据科技有限公司")
    orgs = [h.text for h in hits if h.type == "ORG"]
    assert orgs == ["北京智源人工智能研究院有限公司", "上海云帆数据科技有限公司"] or set(orgs) == {"北京智源人工智能研究院有限公司", "上海云帆数据科技有限公司"}
    for bad in ("甲方", "乙方", "，"):
        assert not any(bad in o for o in orgs)


def test_org_bank():
    d = Detector()
    hits = d.detect("乙方开户行：中国工商银行上海张江支行")
    orgs = [h.text for h in hits if h.type == "ORG"]
    assert "中国工商银行上海张江支行" in orgs


def test_org_no_cross():
    d = Detector()
    hits = d.detect("北京智源人工智能研究院有限公司和上海云帆数据科技有限公司")
    orgs = [h.text for h in hits if h.type == "ORG"]
    assert "北京智源人工智能研究院有限公司" in orgs
    assert "上海云帆数据科技有限公司" in orgs
    assert not any("和" in o and o.count("有限公司") > 1 for o in orgs)

def test_uscc_with_z():
    d = Detector()
    hits = d.detect("91310115MA1K3XYZ7P")
    usccs = {h.text for h in hits if h.type == "USCC"}
    assert "91310115MA1K3XYZ7P" in usccs


def test_uscc_vs_id():
    d = Detector()
    hits = d.detect("110101199001011234")
    ids = {h.text for h in hits if h.type == "ID"}
    usccs = {h.text for h in hits if h.type == "USCC"}
    assert "110101199001011234" in ids
    assert "110101199001011234" not in usccs
