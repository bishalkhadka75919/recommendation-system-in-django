  $(document).ready(function() {
     
      var owl = $("#fashion-product");
     
      owl.owlCarousel({
          items : 7, //10 items above 1000px browser width
          itemsDesktop : [1000,5], //5 items between 1000px and 901px
          itemsDesktopSmall : [900,3], // betweem 900px and 601px
          itemsTablet: [600,2], //2 items between 600 and 0
          itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
		  pagination: false,
      autoPlay:true,
      });
     
      // Custom Navigation Events
      $(".product_next").click(function(){
        owl.trigger('owl.next');
      })
      $(".product_prev").click(function(){
        owl.trigger('owl.prev');
      })
      $(".product_play").click(function(){
        owl.trigger('owl.play',1000); //owl.play event accept autoPlay speed as second parameter
      })
      $(".product_stop").click(function(){
        owl.trigger('owl.stop');
      })
     
    });

/* feature product */
    $(document).ready(function() {
    var owl = $("#featured-products");
    owl.owlCarousel({
          items : 4, //10 items above 1000px browser width
          itemsDesktop : [1000,4], //5 items between 1000px and 901px
          itemsDesktopSmall : [900,2], // betweem 900px and 601px
          itemsTablet: [600,1], //2 items between 600 and 0
          itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
		  pagination: false
      });
       // Custom Navigation Events
      $(".featured_next").click(function(){
        owl.trigger('owl.next');
      })
      $(".featured_prev").click(function(){
        owl.trigger('owl.prev');
      })    
    });

/* feature product */

/* feature product */
$(document).ready(function() {
  var owl = $("#special"),
      status = $("#owlStatus");
  owl.owlCarousel({
	items : 1,
	itemsDesktop : [1000,1], //5 items between 1000px and 901px
    itemsDesktopSmall : [900,1], // betweem 900px and 601px
    itemsTablet: [600,1], //2 items between 600 and 0
    itemsMobile : false ,// itemsMobile disabled - inherit from itemsTablet option
    afterAction : afterAction,
	 pagination: false
  });
  function updateResult(pos,value){
    status.find(pos).find(".result").text(value);
  }
  function afterAction(){
    updateResult(".currentItem", this.owl.currentItem + 1);
    updateResult(".owlItems", this.owl.owlItems.length);
  }
        // Custom Navigation Events
      $(".special_next").click(function(){
        owl.trigger('owl.next');
      })
      $(".special_prev").click(function(){
        owl.trigger('owl.prev');
      })
  });
  /* brand logo */
    $(document).ready(function() {
      var owl = $("#brand-logo");
      owl.owlCarousel({
          items : 5, //10 items above 1000px browser width
          itemsDesktop : [1000,3], //5 items between 1000px and 901px
          itemsDesktopSmall : [900,2], // betweem 900px and 601px
          itemsTablet: [600,1], //2 items between 600 and 0
          itemsMobile : false, // itemsMobile disabled - inherit from itemsTablet option
		   pagination: false
      });
      // Custom Navigation Events
      $(".brand_next").click(function(){
        owl.trigger('owl.next');
      })
      $(".brand_prev").click(function(){
        owl.trigger('owl.prev');
      })
    });

  
  



    