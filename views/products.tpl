<p>{{counter}}</p>
<a href="/products">Home</a><br>
<a href="/cart">Cart</a><br>
<form action="/products" method="post">
    % if product == "page":
        <h2>Products</h2>
        % for x in page:
            % for y in range(int(x[1])):
                <h3>{{heads[x[0]]}}</h3>
                <div style="display: flex; justify-content: space-between; width: 25%;">
                    <img style="width: 75%;" src={{pics[x[0]]}}>
                    <div style="display: flex; flex-flow: column; justify-content: center;">
                        <a href="/cart?rem={{x[0]}}" style="margin: 0;">Remove</a>
                    </div>
                </div>
            % end
        % end
    % elif product != None:
        <input style="display: none;" name="product" type="text" value="{{product}}">
        <h1>{{heads[product]}}</h1>
        <img src={{pics[product]}}>
        <input value="Add" type="submit">
    % else:
        <a href="products/cpu">Processor</a><br>
        <a href="products/gpu">Graphics Cards</a><br>
        <a href="products/mobo">Motherboard</a><br>
        <a href="products/mem">Memory</a><br>
    % end
</form>