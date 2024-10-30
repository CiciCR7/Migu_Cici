import os
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix

def evaluate_predictions(true_label_path, pred_folder, output_folder):
    # 读取真实标签并排序
    with open(true_label_path, "r") as file:
        true_lines = sorted(file.readlines())  # 对所有行排序
        true_labels = []
        for line in true_lines:
            parts = line.strip().split()
            if len(parts) > 1:  # 确保至少有文件名和标签
                true_labels.append(int(parts[1]))
            else:
                print(f"Warning: Skipping malformed line in true labels: {line.strip()}")

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取预测文件夹中的所有txt文件并排序
    pred_files = sorted([f for f in os.listdir(pred_folder) if f.endswith('.txt')])

    # 遍历预测文件夹中的所有txt文件
    for pred_file in pred_files:
        pred_file_path = os.path.join(pred_folder, pred_file)
        
        # 读取预测标签并排序
        with open(pred_file_path, "r") as file:
            pred_lines = sorted(file.readlines())  # 对每行排序
            pred_labels = []
            for line in pred_lines:
                parts = line.strip().split()
                if len(parts) > 1:  # 确保至少有文件名和标签
                    pred_labels.append(int(parts[1]))
                else:
                    print(f"Warning: Skipping malformed line in prediction file {pred_file}: {line.strip()}")

        # 确保预测标签数量与真实标签一致
        if len(pred_labels) != len(true_labels):
            print(f"Error: Mismatch in number of labels for {pred_file}")
            continue
        
        # 计算各项指标
        accuracy = accuracy_score(true_labels, pred_labels)
        recall = recall_score(true_labels, pred_labels, average='macro')
        precision = precision_score(true_labels, pred_labels, average='macro')
        f1 = f1_score(true_labels, pred_labels, average='macro')
        conf_matrix = confusion_matrix(true_labels, pred_labels)

        # 输出结果到文件
        output_file_path = os.path.join(output_folder, f"comparison_{pred_file}")
        with open(output_file_path, "w") as output_file:
            output_file.write(f"Results for {pred_file}:\n")
            output_file.write(f"Accuracy: {accuracy:.4f}\n")
            output_file.write(f"Recall: {recall:.4f}\n")
            output_file.write(f"Precision: {precision:.4f}\n")
            output_file.write(f"F1 Score: {f1:.4f}\n")
            output_file.write("Confusion Matrix:\n")
            output_file.write(f"{conf_matrix}\n")
            
        print(f"Results for {pred_file} saved to {output_file_path}")

# 示例调用
true_label_path = "/appsharedata/wangqiqi/flux_res/Travel_Natural_Scenery_people_classify/true_labels/classify_people_label.txt"  # 真实标签文件路径
pred_folder = "/appsharedata/wangqiqi/flux_res/Travel_Natural_Scenery_people_classify"    # 预测结果文件夹路径
output_folder = "/appsharedata/wangqiqi/flux_res/Travel_Natural_Scenery_people_classify/metric_compare_result"      # 保存对比结果的文件夹路径

evaluate_predictions(true_label_path, pred_folder, output_folder)
