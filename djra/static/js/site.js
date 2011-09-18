function set_top_nav(tab){
  $(".topbar .nav li.active").removeClass('active');
  $(".topbar .nav #top-nav-" + tab).addClass('active');
}
