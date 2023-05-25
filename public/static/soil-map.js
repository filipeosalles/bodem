function draw() {
        const img = document.getElementById('bodemprofiel-img')
        let canvas = document.getElementById('bodemprofiel');
        const ctx = canvas.getContext('2d');
        canvas.width = 1280;
        canvas.height = 1690;
        img.width = 1280;
        img.height = 1690;
        function drawLine(context, x1, y1, x2, y2) {
            context.beginPath();
            context.moveTo(x1, y1);
            context.lineTo(x2, y2);
            context.stroke();
        }
        function drawHead(context, x1, y1, x2, y2, filled) {
            var dx = x2 - x1;
            var dy = y2 - y1;
            context.beginPath();
            context.moveTo(x1 + 0.5 * dy, y1 - 0.5 * dx); // https://dirask.com/posts/jMqM0j
            context.lineTo(x1 - 0.5 * dy, y1 + 0.5 * dx); // https://dirask.com/posts/1GoW61
            context.lineTo(x2, y2);
            context.closePath();
            filled ? context.fill() : context.stroke();
        }
        function drawArrow(context, x1, y1, x2, y2, arrow, filled) {
            if (arrow == null) {
                arrow = 0.1;
            }
            var dx = x2 - x1;
            var dy = y2 - y1;
            var t = 1.0 - arrow;
            var middleX = dx * t + x1;
            var middleY = dy * t + y1;
            drawLine(context, x1, y1, middleX, middleY);
            drawHead(context, middleX, middleY, x2, y2, filled);
        }
        function drawFilledArrow(context, x1, y1, x2, y2, arrow, color, width) {
            context.lineWidth = width;
            context.fillStyle = color;
            context.strokeStyle = color;
            drawArrow(context, x1, y1, x2, y2, arrow, true);
        }
        var factor  = Math.min ( canvas.width / img.width, canvas.height / img.height );

        ctx.scale(factor, factor);
        ctx.drawImage(img, 0, 0);
        ctx.scale(1 / factor, 1 / factor);


        for (i  = 0; i < POSITIONS.length; i++){
            drawFilledArrow(ctx, 0, POSITIONS[i], 40, POSITIONS[i], 0.6, 'gold', 10);
        }

}

function ExportPdf(){
if ($("#name_of_farm").val() == "") {
    alert("Name of farm is required!");
   return
}
$("#soil-report-title").text("Soil report: "+ $("#name_of_farm").val())
kendo.drawing
    .drawDOM("#soil-map-print",
    {
        forcePageBreak: ".page-break",
        paperSize: "A4",
        margin: { top: "1cm", bottom: "2cm", left: "1cm", right: "1cm" },
        scale: 0.8,
        height: 1280,
        template: $("#page-template").html(),
        keepTogether: ".prevent-split"
    })
        .then(function(group){
        kendo.drawing.pdf.saveAs(group, "report-soil-map.pdf")
    });
}

function convertHTMLFileToPDF() {
        return ExportPdf()
       var $print = $('#soil-map-print')
       $print.addClass('pdf')
      html2canvas($print, {
        width: 2480,
      }).then(canvas => {
        try {
            contentH = $('#soil-map-print').height();
            var img = canvas.toDataURL("image/png", 0.8);
            $w = $actw = canvas.width;
            $h = $acth = canvas.height;
            var pdf = new jsPDF("p", "px", "a4");
            var width = $maxw = pdf.internal.pageSize.width;
            var height = $maxh = pdf.internal.pageSize.height;
            if (!$maxw) $maxw = width;
            if (!$maxh) $maxh = height;
            if ($w > $maxw) {
                $w = $maxw;
                $h = Math.round($acth / $actw * $maxw);
            }
            pdf.addImage(img, 'JPEG', 0, 0, $w, $h);
            $count = Math.ceil($h) / Math.ceil($maxh) - 1;
            $count = Math.ceil($count);
            for (var i = 1; i <= $count; i++) {
                position = - $maxh * i
                pdf.addPage(img, 'JPEG', 0, 0, $w, $h);
                pdf.addImage(img, 'JPEG', 0, position, $w, $h);
            }
            pdf.save("cart.pdf");
        } catch (e) {
            alert("Error description: " + e.message);
        }
    });
}

function convertHTMLFileToPDFa() {
	 var container = document.querySelector("#soil-map-print");
    html2canvas(container).then(canvas => {
        let doc = new jsPDF({
            orientation: 'p',
            unit: 'px',
            format: 'a4'
        });
        doc.width = doc.internal.pageSize.width;
        doc.height = doc.internal.pageSize.height;
        doc.margin = {
            horiz: 15,
            vert: 20
        };
        doc.work = {
            width: doc.width - (doc.margin.horiz * 2),
            height: doc.height - (doc.margin.vert * 2)
        }

        let data = {
            width: container.offsetWidth,
            height: container.offsetHeight,
            ctx: canvas.getContext('2d'),
            page: {}
        };
        data.page.width = data.width;
        data.page.height = (data.width*doc.work.height)/doc.work.width;

        const getData = function(imgData, width, height){
            let oCanvas = document.createElement('canvas');
            oCanvas.width=width;
            oCanvas.height=height;
            let oCtx = oCanvas.getContext('2d');
            oCtx.putImageData(imgData, 0, 0);
            return oCanvas.toDataURL('image/png');
        };

        /**/
        let oImgData = null;
        let dataURL = null;
        let pages = Math.ceil(data.height / data.page.height);
        for(let i=0; i<pages; i++){
            if( i!=0 ){
                doc.addPage();
            }
            oImgData = data.ctx.getImageData(0, data.page.height*i, data.page.width, data.page.height);
            dataURL = getData(oImgData, data.page.width, data.page.height);
            doc.addImage(dataURL, 'PNG', doc.margin.horiz, doc.margin.vert, doc.work.width, doc.work.height);
        }
        /**/
        doc.save('Test.pdf');

    });
}

window.addEventListener("load", event => {
    draw()
});




