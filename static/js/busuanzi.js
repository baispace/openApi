!function () {
    var t = ["site_pv", "site_uv", "page_pv", "page_uv"], e = document.currentScript, a = e.hasAttribute("pjax"),
        n = e.getAttribute("data-api") || "https://busuanzi.baispace.cn/api",
        i = e.getAttribute("data-prefix") || "busuanzi", r = "bsz-id", s = function () {
            var e = new XMLHttpRequest;
            e.open("POST", n, !0);
            var a = localStorage.getItem(r);
            null != a && e.setRequestHeader("Authorization", "Bearer " + a), e.setRequestHeader("x-bsz-referer", window.location.href), e.onreadystatechange = function () {
                if (4 === e.readyState && 200 === e.status) {
                    var a = JSON.parse(e.responseText);
                    if (200 == a.code) {
                        t.map((function (t) {
                            var e = document.getElementById("".concat(i, "_").concat(t));
                            null != e && (e.innerHTML = a.data[t]);
                            var n = document.getElementById("".concat(i, "_container_").concat(t));
                            null != n && (n.style.display = "inline")
                        }));
                        var n = e.getResponseHeader("Set-Bsz-Identity");
                        null != n && "" != n && localStorage.setItem(r, n)
                    }
                }
            }, e.send()
        };
    if (s(), a) {
        var o = window.history.pushState;
        window.history.pushState = function () {
            o.apply(this, arguments), s()
        }, window.addEventListener("popstate", (function (t) {
            s()
        }), !1)
    }
}();