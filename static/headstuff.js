doit = function() {
    var c = document.getElementById("space");
    var ctx = c.getContext("2d");
    var n1x=55;
    var n1y=63;
    var nodew=50;
    var sep=150;
    ctx.fillStyle = "#555";
    ctx.strokeStyle = "#555";

    function circ(lw, x,y,w,s) {
        ctx.beginPath();
        ctx.lineWidth=lw;
        ctx.arc(x,y,w,0,2*Math.PI);
        if (s) {
            ctx.stroke();
        }
        else {
            ctx.fill();
        }
    }

    function line(lw, ox,oy,dx,dy) {
        ctx.beginPath();
        ctx.lineWidth=lw;
        ctx.moveTo(ox,oy);
        ctx.lineTo(dx,dy);
        ctx.stroke();
    }

    function rarrow(lw, orx,ory,offx,offy) {
        ctx.beginPath();
        ctx.lineWidth=lw;
        ctx.moveTo(orx, ory);
        ctx.lineTo(orx-offx, ory-offy);
        ctx.lineTo(orx-offx, ory+offy);
        ctx.lineTo(orx, ory);
        ctx.fill();
    }

    function canvas_arrow(fromx, fromy, tox, toy, linewidth, headlen, offset){

        var angle = Math.atan2(toy-fromy,tox-fromx);
        //var angle = Math.acos()
        fromx = fromx + Math.cos(angle)*offset;
        fromy = fromy + Math.sin(angle)*offset;
        tox = tox - Math.cos(angle)*offset*1.1;
        toy = toy - Math.sin(angle)*offset*1.1;
        var adjustX = (tox-fromx)*0.04 + tox;
        var adjustY = (toy-fromy)*0.04 + toy;
        ctx.beginPath();
        console.trace(fromx);
        console.trace(fromy);
        console.trace(angle);
        console.trace(Math.sin(angle));
        ctx.moveTo(fromx, fromy);
        ctx.lineTo(tox, toy);
        ctx.closePath();

        ctx.lineWidth = linewidth;
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(adjustX, adjustY);
        ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
        ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
        ctx.lineTo(adjustX, adjustY);
        ctx.closePath();

        ctx.lineWidth = linewidth;

        ctx.fill();
        ctx.stroke();
    }
    function box(lw, l,t, w, h) {
        ctx.beginPath();
        ctx.lineWidth=lw;
        ctx.moveTo(l, t);
        ctx.lineTo(l+w, t);
        ctx.lineTo(l+w, t+h);
        ctx.lineTo(l, t+h);
        ctx.lineTo(l,t);
        ctx.stroke();
    }

    // first circle
    /*circ(5,n1x,n1y,nodew+1,true);

    // line
    line(10, n1x+nodew, n1y, n1x+nodew+sep-10, n1y);

    // arrow head
    rarrow(2, n1x+nodew+sep+3, n1y, 30, 15);

    // second circle
    circ(2,n1x+nodew*2+sep, n1y, nodew, false);
    */

    var n1x=150;
    var n1y=60;
    var nodew=25;
    var topsep=75;
    var horsep = 40;
    var n2x=n1x+nodew+topsep;
    var n3y=n1y+nodew+horsep;
    var n3x=n1x-nodew*2;
    var n4x=n1x+nodew*2;
    var n5x=n2x+nodew*2;
    circ(3, n1x, n1y, nodew, true);
    circ(3, n2x, n1y, nodew, true);
    circ(3, n3x, n3y, nodew, false);
    circ(3, n4x, n3y, nodew, false);
    circ(3, n5x, n3y, nodew, false);
    box(2, n3x-nodew*1.3, n3y-nodew*1.3, n5x+2*nodew*1.3-n3x, nodew*2*1.3);
    ctx.strokeStyle = "#444";
    canvas_arrow(n1x,n1y, n3x,n3y, 3, 5, nodew);
    canvas_arrow(n1x,n1y, n4x,n3y, 3, 5, nodew);
    canvas_arrow(n2x,n1y, n4x,n3y, 3, 5, nodew);
    canvas_arrow(n2x,n1y, n5x,n3y, 3, 5, nodew);





    // text
    ctx.font="20px monospace";
    ctx.fillText("latent.space", n3x+nodew+5, 20);
    ctx.font="35px monospace";
    //ctx.fillText("Φ", n1x-11, n1y+13);
    ctx.fillStyle="#BBB";
    //ctx.fillText("X", n1x+2*nodew+sep-12, n1y+13);
}
