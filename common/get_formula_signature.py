def get_formula_signature(formula):
    """ Return formula signature for given formula."""
    formula_signature = ""
    oprnd_sign_li = []
    for each_operand_dict in formula:
        table_type = each_operand_dict.get("TABLE_TYPE", '')
        taxo = each_operand_dict.get("TAXO", '')
        ph_val = each_operand_dict.get("PH_VAL", '')
        operator = each_operand_dict.get("OPERATOR", '')
        oprnd_sign_st = "{op}#{tt}.{tx}.{ph}".format(op=operator, tt=table_type, tx=taxo, ph=ph_val)
        oprnd_sign_li.append(oprnd_sign_st)
    formula_signature = "^".join(oprnd_sign_li)
    return formula_signature
