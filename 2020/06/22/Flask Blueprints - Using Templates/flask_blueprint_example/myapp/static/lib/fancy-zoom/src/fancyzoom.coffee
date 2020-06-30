$ = jQuery

$.fn.fancyZoom = (options) ->
  show = (e) ->
    return false  if zooming
    return hide() if zoom.data('el') is this

    zoom_width = options.width
    zoom_height = options.height
    width = $(window).innerWidth()
    height = $(window).innerHeight()
    x = $(window).scrollLeft()
    y = $(window).scrollTop()
    window_size =
      width: width
      height: height
      x: x
      y: y

    width = (zoom_width or @naturalWidth)
    height = (zoom_height or @naturalHeight)

    if window_size.width < width
      new_width = window_size.width - 50
      height *= new_width / width
      width = new_width

    return false if !options.showAlways and (width <= @width or height <= @height)

    # ensure that the top isn't too high and the close button is fully visible
    newTop = Math.max((window_size.height / 2) - (height / 2) + y, 10)
    newLeft = (window_size.width / 2) - (width / 2)
    curTop = e.pageY
    curLeft = e.pageX
    zoom_close.data "curTop", curTop
    zoom_close.data "curLeft", curLeft
    zoom.hide().css
      position: "absolute"
      top: curTop + "px"
      left: curLeft + "px"
      width: "1px"
      height: "1px"

    zoom_close.hide()
    zoom.click hide  if options.closeOnClick

    zoom_content.html $(this).clone()
    zoom_content.children().css width: '100%'

    zoom.animate
      top: newTop + "px"
      left: newLeft + "px"
      opacity: "show"
      width: width
      height: height
    , 500, null, ->
      zoom_close.show()
      zooming = false

    zooming = true
    zoom.data 'el', this
    false
  hide = ->
    return false  if zooming
    zooming = true
    zoom.data 'el', null
    zoom.unbind "click"
    zoom_close.hide()
    zoom.animate
      top: zoom_close.data("curTop") + "px"
      left: zoom_close.data("curLeft") + "px"
      opacity: "hide"
      width: "1px"
      height: "1px"
    , 500, null, ->
      zoom_content.html ""
      zooming = false

    false

  options or= {}
  directory = (if options and options.directory then options.directory else "img")
  zooming = false
  if $("#zoom-box").length is 0
    html = """
    <div id="zoom-box" style="display:none;">
       <div class="zoom-content">
       </div>
       <a href="javascript:void(0)" class="zoom-close">
         <img src="#{directory}/closebox.png" alt="&#215;">
       </a>
     </div>
    """
    $("body").append html
    $("html").click (e) ->
      # Don't handle clicks on the zoom box.
      if zoom.is(':visible') and $(e.target).parents('#zoom-box').length is 0
        hide()
      else
        undefined

    $(document).keyup (event) ->
      hide()  if event.keyCode is 27 and $("#zoom-box:visible").length > 0

    $('#zoom-box > .zoom-close').click hide

  zoom = $('#zoom-box')
  zoom_close = zoom.children('.zoom-close')
  zoom_content = zoom.children('.zoom-content')

  @each (i) ->
    $(this).click show

  return this
