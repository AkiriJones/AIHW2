import sys
from sys import argv
import math

att1 = {}
att2 = {}
att3 = {}
att4 = {}
att5 = {}
att6 = {}
att7 = {}
att8 = {}
attList = [att1, att2, att3, att4, att5, att6, att7, att8]
class_A = set()
class_B = set()


def get_data():
    inputfile = open(args[0])
    class_value = ""
    curr_att = {}
    count = 1
    for line in inputfile:
        line = line.strip().split()
        for i in range(len(line)):
            if i == 0:
                curr_att = att1
            elif i == len(line) - 1:
                if line[i] == "A":
                    class_A.add(count)
                    break
                else:
                    class_B.add(count)
                    break
            else:
                curr_att = attList[i]
            curr_att[count] = line[i]
        count += 1

def entropy(a_count,b_count):
    total = a_count + b_count
    if total == 0:
        return 0
    p_a = a_count / total #probablity of a
    p_b = b_count / total  #probability of b
    ent = 0
    if p_a > 0:
        ent -= p_a * math.log2(p_a)
    if p_b > 0:
        ent -= p_b * math.log2(p_b)
    return ent

def info_gain(att):
    true_a = false_a = true_b = false_b = 0
    for key,value in att.items():
        if value == "True":
            if key in class_A:
                true_a += 1
            elif key in class_B:
                true_b += 1
        elif value == "False":
            if key in class_A:
                false_a += 1
            elif key in class_B:
                false_b += 1
    total_a = len(class_A)
    total_b = len(class_B)
    total = total_a + total_b

    base_entropy = entropy(true_a,false_a)
    true_total = true_a + true_b
    false_total = false_a + false_b

    true_entropy = entropy(true_a,true_b)
    false_entropy = entropy(false_a,false_b)

    weighted_entropy = (true_total / total) * true_entropy + (false_total / total) * false_entropy

    gain = base_entropy - weighted_entropy
    return gain

def info_subset_gain(att,subset_a,subset_b):
    true_a = false_a = true_b = false_b = 0
    subset_ids = set(subset_a).union(subset_b)

    for key,value in att.items():
        if key not in subset_ids:
            continue
        if value == "True":
            if key in subset_a:
                true_a += 1
            elif key in subset_b:
                true_b += 1
        elif value == "False":
            if key in subset_a:
                false_a += 1
            elif key in subset_b:
                false_b += 1

    total_a = len(subset_a)
    total_b = len(subset_b)
    total = total_a + total_b

    base_entropy = entropy(total_a,total_b)

    true_total = true_a + true_b
    false_total = false_a + false_b

    true_entropy = entropy(true_a, true_b)
    false_entropy = entropy(false_a, false_b)

    weighted_entropy = (true_total / total) * true_entropy + (false_total / total) * false_entropy
    gain = base_entropy - weighted_entropy
    return gain

def get_subset(att_dict, value):
    return [key for key, val in att_dict.items() if val == value]

def majority_class(subset_A, subset_B):
    return "A" if len(subset_A) >= len(subset_B) else "B"

if __name__ == '__main__':
    args = argv[1:]
    if len(args) != 1:
        print("Usage: python AIHW3.py DTInput", file=sys.stderr)
        sys.exit(1)
    else:
        get_data()
        print(f"Overall entropy: {entropy(len(class_A), len(class_B)):.4f}")
        #Root index
        root_gain = [info_gain(att) for att in attList]
        root_index = root_gain.index(max(root_gain))
        print(f"Root Attribute: A{root_index + 1}")

        for root_val in ["True", "False"]:
            print(f"\nBranch: A{root_index + 1} = {root_val}")
            subset_ids = get_subset(attList[root_index], root_val)
            subset_a = class_A.intersection(subset_ids)
            subset_b = class_B.intersection(subset_ids)

            local_gains = []
            for i, att in enumerate(attList):
                if i == root_index:
                    local_gains.append(-1)
                    continue
                filtered_att = {k: v for k, v in att.items() if k in subset_ids}
                gain = info_subset_gain(filtered_att, subset_a, subset_b)
                local_gains.append(gain)

            second_index = local_gains.index(max(local_gains))
            print(f"  -> Best Split: A{second_index + 1}")
            for val in ["True", "False"]:
                leaf_ids = [k for k, v in attList[second_index].items()
                            if v == val and k in subset_ids]
                leaf_A = class_A.intersection(leaf_ids)
                leaf_B = class_B.intersection(leaf_ids)
                prediction = majority_class(leaf_A, leaf_B)
                print(f"    If A{second_index + 1} = {val} -> Predict {prediction}")

        # for att in attList:
        #     print(att)
        # print(class_A)
        # print(class_B)


