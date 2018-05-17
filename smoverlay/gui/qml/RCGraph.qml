import QtQuick 2.4

Canvas {
    id: canvas

    property var graphData: ({})

    function posX(x) {
        return canvas.width / ( graphData.length - 1 ) * x
    }

    function posY(y) {
        return canvas.height - canvas.height / graphData.maximum * y
    }

    function draw(ctx) {
        for (var i = 0; i < graphData.datasets.length; i++) {
            var dataset = graphData.datasets[i]
            ctx.strokeStyle = dataset.strokeColor
            ctx.strokeWidth = dataset.strokeWidth
            ctx.fillStyle = dataset.fillColor
            if (dataset.data.length == 0) {
                console.log('no points for dataset ' + i)
                continue
            }
            var data = dataset.data
            ctx.beginPath()
            ctx.moveTo(posX(0), posY(data[0]))
            for (var j = 1; j < data.length; j++) {
                // bezier
                ctx.lineTo(posX(j), posY(data[j]))
            }

            ctx.stroke()

            ctx.lineTo(posX(data.length - 1), posY(0))
            ctx.lineTo(posX(0), posY(0))
            ctx.closePath()

            ctx.fill()
        }
    }

    onPaint: {
        var ctx = canvas.getContext("2d");
        ctx.reset()
        draw(ctx)
    }
}

