from anytree import Node, RenderTree


def build_paths_and_trees(parent_list):
    nodes = {}  # Dictionary to store nodes by id

    # print("Generating paths:")
    # for r in parent_list:
    #     print(r)

    # First pass: create nodes
    for id, name, parent_id in parent_list:
        nodes[id] = Node(name, id=id)

    # Second pass: attach parent-child relationships
    for id, name, parent_id in parent_list:
        if parent_id is not None:
            nodes[id].parent = nodes[parent_id]

    # print the tree structure
    # roots = [node for node in nodes.values() if node.is_root]
    # for root in roots:
    #     for pre, fill, node in RenderTree(root):
    #         print(f"{pre}{node.name} ({node.id})")

    # Build a list of category paths from root to each node
    category_paths = []
    for node in nodes.values():
        path = ": ".join([ancestor.name for ancestor in node.path])
        category_path = [node.id, path]
        category_paths.append(category_path)
    
    # Sort paths alphabetically
    category_paths.sort(key = lambda x: x[1].lower())
    # print('\nPaths:')
    # for p in category_paths:
    #     print(p)
    return category_paths