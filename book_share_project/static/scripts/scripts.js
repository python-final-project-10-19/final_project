
window.onload = function test(context) {
    //print(`${process.env('DEV_SITE')}/books/post`)
    console.log('MADE IT HERE')
    $.ajax({
      type: "POST",
      url: `${process.env('DEV_SITE')}/books/post`,
      data: context,
      success: $('#add-button').after( "<span>Added to your collection</span>" ),
      });
  }

// function test(context) {
//     console.log(context);
// }
