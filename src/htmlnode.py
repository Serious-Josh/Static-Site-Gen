

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if len(self.props) == 0 or self.props is None: # type: ignore
            return ""
        
        string = " "

        for item in self.props:
            string += f'{item}="{self.props[item]}" '

        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode: No value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode: No tag")
        elif self.children is None:
            raise ValueError("ParentNode: No children")
        
        children = ""

        for each in self.children:
            children += each.to_html()
        
        return f"<{self.tag}>{children}</{self.tag}>" 