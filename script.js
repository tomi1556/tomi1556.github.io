var slideshowDuration = 4000;
var slideshow = $(".main-content .slideshow");
var windowHeight = $(window).height(); // ウィンドウの初期高さを取得

function slideshowSwitch(slideshow, index, auto) {
  if (slideshow.data("wait")) return;

  var slides = slideshow.find(".slide");
  var activeSlide = slides.filter(".is-active");
  var newSlide = slides.eq(index);
  
  if (newSlide.is(activeSlide)) return;

  newSlide.addClass("is-new");
  var timeout = slideshow.data("timeout");
  clearTimeout(timeout);
  slideshow.data("wait", true);
  var transition = slideshow.attr("data-transition");
  
  if (transition == "fade") {
    newSlide.css({ display: "block", opacity: 0 });
    TweenMax.to(newSlide, 1, {
      opacity: 1,
      onComplete: function () {
        newSlide.addClass("is-active").removeClass("is-new");
        activeSlide.removeClass("is-active").css({ display: "none" });
        slideshow.data("wait", false);
        if (auto) {
          timeout = setTimeout(function () {
            slideshowNext(slideshow, false, true);
          }, slideshowDuration);
          slideshow.data("timeout", timeout);
        }
      }
    });
  } else {
    var newSlideRight = (newSlide.index() > activeSlide.index()) ? 0 : "auto";
    var newSlideLeft = (newSlide.index() > activeSlide.index()) ? "auto" : 0;
    var activeSlideImageLeft = (newSlide.index() > activeSlide.index()) ? -slideshow.width() : slideshow.width();

    newSlide.css({
      display: "block",
      left: (newSlide.index() > activeSlide.index()) ? "100%" : "-100%",
      zIndex: 2
    });

    TweenMax.to(activeSlide, 1, {
      left: activeSlideImageLeft,
      ease: Power3.easeInOut
    });

    TweenMax.to(newSlide, 1, {
      left: 0,
      ease: Power3.easeInOut,
      onComplete: function () {
        newSlide.addClass("is-active").removeClass("is-new");
        activeSlide.removeClass("is-active").css({ display: "none" });
        slideshow.data("wait", false);
        if (auto) {
          timeout = setTimeout(function () {
            slideshowNext(slideshow, false, true);
          }, slideshowDuration);
          slideshow.data("timeout", timeout);
        }
      }
    });
  }
}



function slideshowNext(slideshow, previous, auto) {
  var slides = slideshow.find(".slide");
  var activeSlide = slides.filter(".is-active");
  var newSlide = null;
  if (previous) {
    newSlide = activeSlide.prev(".slide");
    if (newSlide.length === 0) {
      newSlide = slides.last();
    }
  } else {
    newSlide = activeSlide.next(".slide");
    if (newSlide.length == 0) newSlide = slides.filter(".slide").first();
  }

  slideshowSwitch(slideshow, newSlide.index(), auto);
}

function homeSlideshowParallax() {
  var scrollTop = $(window).scrollTop();
  if (scrollTop > windowHeight) return;
  var inner = slideshow.find(".slideshow-inner");
  var newHeight = windowHeight - scrollTop / 2;
  var newTop = scrollTop * 0.8;

  inner.css({
    transform: "translateY(" + newTop + "px)",
    height: newHeight
  });
}

$(document).ready(function () {
  $(".slide").addClass("is-loaded");

  $(".slideshow .arrows .arrow").on("click", function () {
    slideshowNext($(this).closest(".slideshow"), $(this).hasClass("prev"));
  });

  $(".slideshow .pagination .item").on("click", function () {
    slideshowSwitch($(this).closest(".slideshow"), $(this).index());
  });

  $(".slideshow .pagination").on("check", function () {
    var slideshow = $(this).closest(".slideshow");
    var pages = $(this).find(".item");
    var index = slideshow.find(".slides .is-active").index();
    pages.removeClass("is-active");
    pages.eq(index).addClass("is-active");
  });

  /* Lazyloading
$('.slideshow').each(function(){
  var slideshow=$(this);
  var images=slideshow.find('.image').not('.is-loaded');
  images.on('loaded',function(){
    var image=$(this);
    var slide=image.closest('.slide');
    slide.addClass('is-loaded');
  });
*/

  var timeout = setTimeout(function () {
    slideshowNext(slideshow, false, true);
  }, slideshowDuration);

  slideshow.data("timeout", timeout);
});

if ($(".main-content .slideshow").length > 1) {
  $(window).on("scroll", homeSlideshowParallax);
}


async function fetchOnlineUsers() {
    try {
        const response = await fetch('https://mcapi.us/server/status?ip=stella.xgames.jp');
        const data = await response.json();
        document.getElementById('online-users').textContent = data.players.now;

        const onlinePlayers = document.getElementById('online-players');
        onlinePlayers.innerHTML = '';

        if (data.players && data.players.now > 0 && data.players.sample) {
            data.players.sample.forEach(player => {
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player';

                const playerImg = document.createElement('img');
                playerImg.src = `https://mc-heads.net/avatar/${player.id}/100`;

                const playerId = document.createElement('p');
                playerId.textContent = player.name;

                playerDiv.appendChild(playerImg);
                playerDiv.appendChild(playerId);
                onlinePlayers.appendChild(playerDiv);
            });
        } else {
            onlinePlayers.textContent = '現在オンラインのプレイヤーはいません。';
        }
    } catch (error) {
        console.error('エラー:', error);
        document.getElementById('online-players').textContent = 'オンラインのユーザー数を取得できませんでした';
    }
}

fetchOnlineUsers();
setInterval(fetchOnlineUsers, 60000);


function copyToClipboard(address, button) {
    navigator.clipboard.writeText(address).then(() => {
        button.textContent = '完了！';
        button.classList.add('copy-success');
        setTimeout(() => {
            button.textContent = 'コピー';
            button.classList.remove('copy-success');
        }, 2000);
    }).catch(err => {
        console.error('エラー:', err);
        button.textContent = 'エラー';
        button.classList.add('copy-fail');
        setTimeout(() => {
            button.textContent = 'コピー';
            button.classList.remove('copy-fail');
        }, 2000);
    });
}
