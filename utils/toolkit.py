import os
import numpy as np
import torch


def count_parameters(model, trainable=False):
    if trainable:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    return sum(p.numel() for p in model.parameters())


def tensor2numpy(x):
    return x.cpu().data.numpy() if x.is_cuda else x.data.numpy()


def target2onehot(targets, n_classes):
    onehot = torch.zeros(targets.shape[0], n_classes).to(targets.device)
    onehot.scatter_(dim=1, index=targets.long().view(-1, 1), value=1.0)
    return onehot


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def accuracy(y_pred, y_true, nb_old, init_cls=10, increment=10):
    assert len(y_pred) == len(y_true), "Data length error."
    all_acc = {}
    all_acc["total"] = np.around(
        (y_pred == y_true).sum() * 100 / len(y_true), decimals=2
    )

    # Grouped accuracy, for initial classes
    idxes = np.where(
        np.logical_and(y_true >= 0, y_true < init_cls)
    )[0]
    label = "{}-{}".format(
        str(0).rjust(2, "0"), str(init_cls - 1).rjust(2, "0")
    )
    all_acc[label] = np.around(
        (y_pred[idxes] == y_true[idxes]).sum() * 100 / len(idxes), decimals=2
    )
    # for incremental classes
    for class_id in range(init_cls, np.max(y_true), increment):
        idxes = np.where(
            np.logical_and(y_true >= class_id, y_true < class_id + increment)
        )[0]
        label = "{}-{}".format(
            str(class_id).rjust(2, "0"), str(class_id + increment - 1).rjust(2, "0")
        )
        all_acc[label] = np.around(
            (y_pred[idxes] == y_true[idxes]).sum() * 100 / len(idxes), decimals=2
        )

    # Old accuracy
    idxes = np.where(y_true < nb_old)[0]

    all_acc["old"] = (
        0
        if len(idxes) == 0
        else np.around(
            (y_pred[idxes] == y_true[idxes]).sum() * 100 / len(idxes), decimals=2
        )
    )

    # New accuracy
    idxes = np.where(y_true >= nb_old)[0]
    all_acc["new"] = np.around(
        (y_pred[idxes] == y_true[idxes]).sum() * 100 / len(idxes), decimals=2
    )

    return all_acc

from sklearn.metrics import f1_score

def f1_score_custom(y_pred, y_true, nb_old, init_cls=10, increment=10):
    assert len(y_pred) == len(y_true), "Data length error."
    all_f1 = {}

    # Total F1 score
    all_f1["total"] = np.around(f1_score(y_true, y_pred, average='weighted'), decimals=2)

    # Grouped F1 score for initial classes
    idxes = np.where(np.logical_and(y_true >= 0, y_true < init_cls))[0]
    label = "{}-{}".format(str(0).rjust(2, "0"), str(init_cls - 1).rjust(2, "0"))
    all_f1[label] = np.around(f1_score(y_true[idxes], y_pred[idxes], average='weighted'), decimals=2)

    # For incremental classes
    for class_id in range(init_cls, np.max(y_true), increment):
        idxes = np.where(np.logical_and(y_true >= class_id, y_true < class_id + increment))[0]
        label = "{}-{}".format(str(class_id).rjust(2, "0"), str(class_id + increment - 1).rjust(2, "0"))
        all_f1[label] = np.around(f1_score(y_true[idxes], y_pred[idxes], average='weighted'), decimals=2)

    # Old F1 score
    idxes = np.where(y_true < nb_old)[0]
    all_f1["old"] = 0 if len(idxes) == 0 else np.around(f1_score(y_true[idxes], y_pred[idxes], average='weighted'), decimals=2)

    # New F1 score
    idxes = np.where(y_true >= nb_old)[0]
    all_f1["new"] = np.around(f1_score(y_true[idxes], y_pred[idxes], average='weighted'), decimals=2)

    return all_f1


from sklearn.metrics import matthews_corrcoef
import numpy as np

def mcc_score_custom(y_pred, y_true, nb_old, init_cls=10, increment=10):
    assert len(y_pred) == len(y_true), "Data length error."
    all_mcc = {}

    # Total MCC score
    all_mcc["total"] = np.around(matthews_corrcoef(y_true, y_pred), decimals=2)

    # Grouped MCC score for initial classes
    idxes = np.where(np.logical_and(y_true >= 0, y_true < init_cls))[0]
    label = "{}-{}".format(str(0).rjust(2, "0"), str(init_cls - 1).rjust(2, "0"))
    all_mcc[label] = np.around(matthews_corrcoef(y_true[idxes], y_pred[idxes]), decimals=2)

    # For incremental classes
    for class_id in range(init_cls, np.max(y_true), increment):
        idxes = np.where(np.logical_and(y_true >= class_id, y_true < class_id + increment))[0]
        label = "{}-{}".format(str(class_id).rjust(2, "0"), str(class_id + increment - 1).rjust(2, "0"))
        all_mcc[label] = np.around(matthews_corrcoef(y_true[idxes], y_pred[idxes]), decimals=2)

    # Old MCC score
    idxes = np.where(y_true < nb_old)[0]
    all_mcc["old"] = 0 if len(idxes) == 0 else np.around(matthews_corrcoef(y_true[idxes], y_pred[idxes]), decimals=2)

    # New MCC score
    idxes = np.where(y_true >= nb_old)[0]
    all_mcc["new"] = np.around(matthews_corrcoef(y_true[idxes], y_pred[idxes]), decimals=2)

    return all_mcc

from sklearn.metrics import cohen_kappa_score

def kappa_score_custom(y_pred, y_true, nb_old, init_cls=10, increment=10):
    assert len(y_pred) == len(y_true), "Data length error."
    all_kappa = {}

    # Total Kappa score
    all_kappa["total"] = np.around(cohen_kappa_score(y_true, y_pred), decimals=2)

    # Grouped Kappa score for initial classes
    idxes = np.where(np.logical_and(y_true >= 0, y_true < init_cls))[0]
    label = "{}-{}".format(str(0).rjust(2, "0"), str(init_cls - 1).rjust(2, "0"))
    all_kappa[label] = np.around(cohen_kappa_score(y_true[idxes], y_pred[idxes]), decimals=2)

    # For incremental classes
    for class_id in range(init_cls, np.max(y_true), increment):
        idxes = np.where(np.logical_and(y_true >= class_id, y_true < class_id + increment))[0]
        label = "{}-{}".format(str(class_id).rjust(2, "0"), str(class_id + increment - 1).rjust(2, "0"))
        all_kappa[label] = np.around(cohen_kappa_score(y_true[idxes], y_pred[idxes]), decimals=2)

    # Old Kappa score
    idxes = np.where(y_true < nb_old)[0]
    all_kappa["old"] = 0 if len(idxes) == 0 else np.around(cohen_kappa_score(y_true[idxes], y_pred[idxes]), decimals=2)

    # New Kappa score
    idxes = np.where(y_true >= nb_old)[0]
    all_kappa["new"] = np.around(cohen_kappa_score(y_true[idxes], y_pred[idxes]), decimals=2)

    return all_kappa


def split_images_labels(imgs):
    # split trainset.imgs in ImageFolder
    images = []
    labels = []
    for item in imgs:
        images.append(item[0])
        labels.append(item[1])

    return np.array(images), np.array(labels)
