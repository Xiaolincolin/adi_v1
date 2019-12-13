webpackJsonp([2], {
    0: function(t, e, n) {
        n("GNx1"),
        n("W+5A"),
        n("uuti"),
        t.exports = n("qIm6")
    },
    GNx1: function(t, e, n) {
        "use strict";
        var r = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
            return typeof t
        }
        : function(t) {
            return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
        }
        ;
        n("ZHmC"),
        n("uBex"),
        n("kss0"),
        n("LKAf"),
        n("j815"),
        window.SysTool = {
            setData: function(t, e) {
                "object" === (void 0 === e ? "undefined" : r(e)) && (e = JSON.stringify(e)),
                window.localStorage.setItem(t, e)
            },
            getData: function(t) {
                return window.localStorage.getItem(t)
            },
            getCookie: function(t) {
                var e, n = new RegExp("(^| )" + t + "=([^;]*)(;|$)");
                return (e = document.cookie.match(n)) ? e[2] : null
            },
            setCookie: function(t, e, n) {
                var r = new Date;
                r.setDate(r.getDate() + n),
                document.cookie = t + "=" + escape(e) + (null == n ? "" : ";expires=" + r.toGMTString())
            },
            removeData: function(t) {
                window.localStorage.removeItem(t)
            },
            arrayToObject: function(t) {
                return t.map(function(t) {
                    return {
                        id: t,
                        name: t
                    }
                })
            },
            arrayToOrder: function(t, e) {
                return "desc" == (arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "asc") ? t.sort(function(t, n) {
                    return t[e] == n[e] ? 0 : t[e] > n[e] ? -1 : 1
                }) : t.sort(function(t, n) {
                    return t[e] == n[e] ? 0 : t[e] > n[e] ? 1 : -1
                })
            },
            mergeArray: function() {
                return Array.prototype.concat.apply([], arguments)
            },
            numFixed: function(t) {
                var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 2;
                return isNaN(t) ? 0 : Number(Number(t).toFixed(e))
            },
            splitString: function(t, e) {
                for (var n = "", r = 0, a = new RegExp(/[^\x00-\xff]/), u = 0; u < t.length; u++) {
                    var o = t.charAt(u);
                    r += a.test(o) ? 2 : 1,
                    r <= e && (n += o)
                }
                return {
                    str: n,
                    len: r
                }
            },
            toFixedValue: function(t) {
                return t > 999 & t < 1e4 ? (t / 1e3).toFixed(1).toString() + "k" : t >= 1e4 && t < 1e6 ? (t / 1e4).toFixed(1).toString() + "w" : t >= 1e6 && t < 1e9 ? (t / 1e6).toFixed(1).toString() + "m" : t >= 1e9 ? (t / 1e9).toFixed(1).toString() + "b" : t
            },
            randomNum: function(t, e) {
                return Math.floor(Math.random() * (e - t + 1) + t)
            }
        },
        Array.prototype.sum = function() {
            return this && 0 != this.length ? this.reduce(function(t, e) {
                return t + e
            }) : 0
        }
    },
    LKAf: function(t, e) {},
    "W+5A": function(t, e, n) {
        "use strict";
        !function() {
            function t(t, e) {
                for (t = String(t); t.length < e; )
                    t = "0" + t;
                return t
            }
            function e(t, e) {
                void 0 === Date.prototype[t] && (Date.prototype[t] = e)
            }
            var n = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
              , r = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
              , a = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
              , u = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
              , o = {
                su: 0,
                sun: 0,
                sunday: 0,
                mo: 1,
                mon: 1,
                monday: 1,
                tu: 2,
                tue: 2,
                tuesday: 2,
                we: 3,
                wed: 3,
                wednesday: 3,
                th: 4,
                thu: 4,
                thursday: 4,
                fr: 5,
                fri: 5,
                friday: 5,
                sa: 6,
                sat: 6,
                saturday: 6
            }
              , i = r.concat(n)
              , s = ["su", "sun", "sunday", "mo", "mon", "monday", "tu", "tue", "tuesday", "we", "wed", "wednesday", "th", "thu", "thursday", "fr", "fri", "friday", "sa", "sat", "saturday"]
              , l = {
                jan: 0,
                january: 0,
                feb: 1,
                february: 1,
                mar: 2,
                march: 2,
                apr: 3,
                april: 3,
                may: 4,
                jun: 5,
                june: 5,
                jul: 6,
                july: 6,
                aug: 7,
                august: 7,
                sep: 8,
                september: 8,
                oct: 9,
                october: 9,
                nov: 10,
                november: 10,
                dec: 11,
                december: 11
            }
              , g = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
              , c = function(t) {
                return !!t.match(/^(\d+)$/)
            }
              , f = function(t, e, n, r) {
                for (var a = r; a >= n; a--) {
                    var u = t.substring(e, e + a);
                    if (u.length < n)
                        return null;
                    if (c(u))
                        return u
                }
                return null
            }
              , h = Date.parse
              , d = function(t, e) {
                t += "",
                e += "";
                for (var n, r, a = 0, u = 0, o = "", l = "", g = new Date, c = g.getYear(), h = g.getMonth() + 1, d = 1, m = 0, v = 0, y = 0, M = ""; u < e.length; ) {
                    for (o = e.charAt(u),
                    l = ""; e.charAt(u) === o && u < e.length; )
                        l += e.charAt(u++);
                    if ("yyyy" === l || "yy" === l || "y" === l) {
                        if ("yyyy" === l && (n = 4,
                        r = 4),
                        "yy" === l && (n = 2,
                        r = 2),
                        "y" === l && (n = 2,
                        r = 4),
                        null === (c = f(t, a, n, r)))
                            return NaN;
                        a += c.length,
                        2 === c.length && (c = c > 70 ? c - 0 + 1900 : c - 0 + 2e3)
                    } else if ("MMM" === l || "NNN" === l) {
                        h = 0;
                        for (var D = 0; D < i.length; D++) {
                            var T = i[D];
                            if (t.substring(a, a + T.length).toLowerCase() === T.toLowerCase() && ("MMM" === l || "NNN" === l && D > 11)) {
                                h = D + 1,
                                h > 12 && (h -= 12),
                                a += T.length;
                                break
                            }
                        }
                        if (h < 1 || h > 12)
                            return NaN
                    } else if ("EE" === l || "E" === l)
                        for (var x = 0; x < s.length; x++) {
                            var p = s[x];
                            if (t.substring(a, a + p.length).toLowerCase() === p.toLowerCase()) {
                                a += p.length;
                                break
                            }
                        }
                    else if ("MM" === l || "M" === l) {
                        if (null === (h = f(t, a, l.length, 2)) || h < 1 || h > 12)
                            return NaN;
                        a += h.length
                    } else if ("dd" === l || "d" === l) {
                        if (null === (d = f(t, a, l.length, 2)) || d < 1 || d > 31)
                            return NaN;
                        a += d.length
                    } else if ("hh" === l || "h" === l) {
                        if (null === (m = f(t, a, l.length, 2)) || m < 1 || m > 12)
                            return NaN;
                        a += m.length
                    } else if ("HH" === l || "H" === l) {
                        if (null === (m = f(t, a, l.length, 2)) || m < 0 || m > 23)
                            return NaN;
                        a += m.length
                    } else if ("KK" === l || "K" === l) {
                        if (null === (m = f(t, a, l.length, 2)) || m < 0 || m > 11)
                            return NaN;
                        a += m.length
                    } else if ("kk" === l || "k" === l) {
                        if (null === (m = f(t, a, l.length, 2)) || m < 1 || m > 24)
                            return NaN;
                        a += m.length,
                        m--
                    } else if ("mm" === l || "m" === l) {
                        if (null === (v = f(t, a, l.length, 2)) || v < 0 || v > 59)
                            return NaN;
                        a += v.length
                    } else if ("ss" === l || "s" === l) {
                        if (null === (y = f(t, a, l.length, 2)) || y < 0 || y > 59)
                            return NaN;
                        a += y.length
                    } else if ("a" === l) {
                        if ("am" === t.substring(a, a + 2).toLowerCase())
                            M = "AM";
                        else {
                            if ("pm" !== t.substring(a, a + 2).toLowerCase())
                                return NaN;
                            M = "PM"
                        }
                        a += 2
                    } else {
                        if (t.substring(a, a + l.length) !== l)
                            return NaN;
                        a += l.length
                    }
                }
                if (a !== t.length)
                    return NaN;
                if (2 === h)
                    if (c % 4 == 0 && c % 100 != 0 || c % 400 == 0) {
                        if (d > 29)
                            return NaN
                    } else if (d > 28)
                        return NaN;
                return (4 === h || 6 === h || 9 === h || 11 === h) && d > 30 ? NaN : (m < 12 && "PM" === M ? m = m - 0 + 12 : m > 11 && "AM" === M && (m -= 12),
                new Date(c,h - 1,d,m,v,y).getTime())
            };
            Date.parse = function(t, e) {
                if (e)
                    return d(t, e);
                var n, r = h(t), a = 0;
                return isNaN(r) && (n = /^(\d{4}|[+\-]\d{6})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{3,}))?)?(?:(Z)|([+\-])(\d{2})(?::?(\d{2}))?))?/.exec(t)) && ("Z" !== n[8] && (a = 60 * +n[10] + +n[11],
                "+" === n[9] && (a = 0 - a)),
                n[7] = n[7] || "000",
                r = Date.UTC(+n[1], +n[2] - 1, +n[3], +n[4], +n[5] + a, +n[6], +n[7].substr(0, 3))),
                r
            }
            ,
            Date.today = function() {
                return (new Date).clearTime()
            }
            ,
            Date.UTCtoday = function() {
                return (new Date).clearUTCTime()
            }
            ,
            Date.tomorrow = function() {
                return Date.today().add({
                    days: 1
                })
            }
            ,
            Date.UTCtomorrow = function() {
                return Date.UTCtoday().add({
                    days: 1
                })
            }
            ,
            Date.yesterday = function() {
                return Date.today().add({
                    days: -1
                })
            }
            ,
            Date.UTCyesterday = function() {
                return Date.UTCtoday().add({
                    days: -1
                })
            }
            ,
            Date.validateDay = function(t, e, n) {
                var r = new Date(e,n,t);
                return r.getFullYear() === e && r.getMonth() === n && r.getDate() === t
            }
            ,
            Date.validateYear = function(t) {
                return t >= 0 && t <= 9999
            }
            ,
            Date.validateSecond = function(t) {
                return t >= 0 && t < 60
            }
            ,
            Date.validateMonth = function(t) {
                return t >= 0 && t < 12
            }
            ,
            Date.validateMinute = function(t) {
                return t >= 0 && t < 60
            }
            ,
            Date.validateMillisecond = function(t) {
                return t >= 0 && t < 1e3
            }
            ,
            Date.validateHour = function(t) {
                return t >= 0 && t < 24
            }
            ,
            Date.compare = function(t, e) {
                return t.valueOf() < e.valueOf() ? -1 : t.valueOf() > e.valueOf() ? 1 : 0
            }
            ,
            Date.equals = function(t, e) {
                return t.valueOf() === e.valueOf()
            }
            ,
            Date.getDayNumberFromName = function(t) {
                return o[t.toLowerCase()]
            }
            ,
            Date.getMonthNumberFromName = function(t) {
                return l[t.toLowerCase()]
            }
            ,
            Date.isLeapYear = function(t) {
                return 29 === new Date(t,1,29).getDate()
            }
            ,
            Date.getDaysInMonth = function(t, e) {
                return 1 === e ? Date.isLeapYear(t) ? 29 : 28 : g[e]
            }
            ,
            e("getMonthAbbr", function() {
                return n[this.getMonth()]
            }),
            e("getMonthName", function() {
                return r[this.getMonth()]
            }),
            e("getUTCOffset", function() {
                var e = t(Math.abs(this.getTimezoneOffset() / .6), 4);
                return this.getTimezoneOffset() > 0 && (e = "-" + e),
                e
            }),
            e("toCLFString", function() {
                return t(this.getDate(), 2) + "/" + this.getMonthAbbr() + "/" + this.getFullYear() + ":" + t(this.getHours(), 2) + ":" + t(this.getMinutes(), 2) + ":" + t(this.getSeconds(), 2) + " " + this.getUTCOffset()
            }),
            e("toYMD", function(e) {
                return e = void 0 === e ? "-" : e,
                this.getFullYear() + e + t(this.getMonth() + 1, 2) + e + t(this.getDate(), 2)
            }),
            e("toDBString", function() {
                return this.getUTCFullYear() + "-" + t(this.getUTCMonth() + 1, 2) + "-" + t(this.getUTCDate(), 2) + " " + t(this.getUTCHours(), 2) + ":" + t(this.getUTCMinutes(), 2) + ":" + t(this.getUTCSeconds(), 2)
            }),
            e("clearTime", function() {
                return this.setHours(0),
                this.setMinutes(0),
                this.setSeconds(0),
                this.setMilliseconds(0),
                this
            }),
            e("clearUTCTime", function() {
                return this.setUTCHours(0),
                this.setUTCMinutes(0),
                this.setUTCSeconds(0),
                this.setUTCMilliseconds(0),
                this
            }),
            e("add", function(t) {
                return void 0 !== t.milliseconds && this.setMilliseconds(this.getMilliseconds() + t.milliseconds),
                void 0 !== t.seconds && this.setSeconds(this.getSeconds() + t.seconds),
                void 0 !== t.minutes && this.setMinutes(this.getMinutes() + t.minutes),
                void 0 !== t.hours && this.setHours(this.getHours() + t.hours),
                void 0 !== t.days && this.setDate(this.getDate() + t.days),
                void 0 !== t.weeks && this.setDate(this.getDate() + 7 * t.weeks),
                void 0 !== t.months && this.setMonth(this.getMonth() + t.months),
                void 0 !== t.years && this.setFullYear(this.getFullYear() + t.years),
                this
            }),
            e("addMilliseconds", function(t) {
                return this.add({
                    milliseconds: t
                })
            }),
            e("addSeconds", function(t) {
                return this.add({
                    seconds: t
                })
            }),
            e("addMinutes", function(t) {
                return this.add({
                    minutes: t
                })
            }),
            e("addHours", function(t) {
                return this.add({
                    hours: t
                })
            }),
            e("addDays", function(t) {
                return this.add({
                    days: t
                })
            }),
            e("addWeeks", function(t) {
                return this.add({
                    days: 7 * t
                })
            }),
            e("addMonths", function(t) {
                return this.add({
                    months: t
                })
            }),
            e("addYears", function(t) {
                return this.add({
                    years: t
                })
            }),
            e("setTimeToNow", function() {
                var t = new Date;
                this.setMilliseconds(t.getMilliseconds()),
                this.setSeconds(t.getSeconds()),
                this.setMinutes(t.getMinutes()),
                this.setHours(t.getHours())
            }),
            e("clone", function() {
                return new Date(this.valueOf())
            }),
            e("between", function(t, e) {
                return this.valueOf() >= t.valueOf() && this.valueOf() <= e.valueOf()
            }),
            e("compareTo", function(t) {
                return Date.compare(this, t)
            }),
            e("equals", function(t) {
                return Date.equals(this, t)
            }),
            e("isAfter", function(t) {
                return t = t || new Date,
                this.compareTo(t) > 0
            }),
            e("isBefore", function(t) {
                return t = t || new Date,
                this.compareTo(t) < 0
            }),
            e("getDaysBetween", function(t) {
                return (t.clone().valueOf() - this.valueOf()) / 864e5 | 0
            }),
            e("getHoursBetween", function(t) {
                return (t.clone().valueOf() - this.valueOf()) / 36e5 | 0
            }),
            e("getMinutesBetween", function(t) {
                return (t.clone().valueOf() - this.valueOf()) / 6e4 | 0
            }),
            e("getSecondsBetween", function(t) {
                return (t.clone().valueOf() - this.valueOf()) / 1e3 | 0
            }),
            e("getMillisecondsBetween", function(t) {
                return t.clone().valueOf() - this.valueOf() | 0
            }),
            e("getOrdinalNumber", function() {
                return Math.ceil((this.clone().clearTime() - new Date(this.getFullYear(),0,1)) / 864e5) + 1
            }),
            e("toFormat", function(t) {
                return m(t, v(this))
            }),
            e("toUTCFormat", function(t) {
                return m(t, y(this))
            });
            var m = function(t, e) {
                var n, r, a, u = [t];
                for (n in e)
                    !function(t, e) {
                        for (var n, r, a, o = 0, i = u.length, s = []; o < i; o++)
                            if ("string" == typeof u[o]) {
                                for (a = u[o].split(t),
                                n = 0,
                                r = a.length - 1; n < r; n++)
                                    s.push(a[n]),
                                    s.push([e]);
                                s.push(a[r])
                            } else
                                s.push(u[o]);
                        u = s
                    }(n, e[n]);
                for (a = "",
                n = 0,
                r = u.length; n < r; n++)
                    a += "string" == typeof u[n] ? u[n] : u[n][0];
                return u.join("")
            }
              , v = function(e) {
                var o = e.getHours() % 12 ? e.getHours() % 12 : 12;
                return {
                    YYYY: e.getFullYear(),
                    YY: String(e.getFullYear()).slice(-2),
                    MMMM: r[e.getMonth()],
                    MMM: n[e.getMonth()],
                    MM: t(e.getMonth() + 1, 2),
                    MI: t(e.getMinutes(), 2),
                    M: e.getMonth() + 1,
                    DDDD: u[e.getDay()],
                    DDD: a[e.getDay()],
                    DD: t(e.getDate(), 2),
                    D: e.getDate(),
                    HH24: t(e.getHours(), 2),
                    HH: t(o, 2),
                    H: o,
                    SS: t(e.getSeconds(), 2),
                    PP: e.getHours() >= 12 ? "PM" : "AM",
                    P: e.getHours() >= 12 ? "pm" : "am",
                    LL: t(e.getMilliseconds(), 3)
                }
            }
              , y = function(e) {
                var o = e.getUTCHours() % 12 ? e.getUTCHours() % 12 : 12;
                return {
                    YYYY: e.getUTCFullYear(),
                    YY: String(e.getUTCFullYear()).slice(-2),
                    MMMM: r[e.getUTCMonth()],
                    MMM: n[e.getUTCMonth()],
                    MM: t(e.getUTCMonth() + 1, 2),
                    MI: t(e.getUTCMinutes(), 2),
                    M: e.getUTCMonth() + 1,
                    DDDD: u[e.getUTCDay()],
                    DDD: a[e.getUTCDay()],
                    DD: t(e.getUTCDate(), 2),
                    D: e.getUTCDate(),
                    HH24: t(e.getUTCHours(), 2),
                    HH: t(o, 2),
                    H: o,
                    SS: t(e.getUTCSeconds(), 2),
                    PP: e.getUTCHours() >= 12 ? "PM" : "AM",
                    P: e.getUTCHours() >= 12 ? "pm" : "am",
                    LL: t(e.getUTCMilliseconds(), 3)
                }
            }
        }()
    },
    ZHmC: function(t, e) {},
    j815: function(t, e) {},
    kss0: function(t, e) {},
    qIm6: function(t, e, n) {
        "use strict";
        !function(t) {
            var e = {
                isNull: "必填",
                errorLetter: "含特殊字符或过长",
                errorLength: "40字符以内",
                lowLetter: "输入小写字母",
                errorEmail: "请输入48位以内的正确邮箱",
                errorNum: "输入数字",
                errorPwd: "6-18位至少包含数字、大小写字母的两种",
                errorUrl: "以http://或https://开头的合法url",
                errorName: "名称不合法或过长",
                errorMoney: "金额格式不对",
                errorQQ: "请输入正确QQ号码",
                errorCompany: "公司名称，支持48位内汉字或96位内字母数字",
                errorUsername: "您的姓名，支持16位内汉字或32位内字母数字",
                errorWechat: "6-20位数字，字母，下划线或中划线，须以数字或字母开头"
            }
              , n = function(t) {
                if (!t.val)
                    return t.nullTxt || "必填";
                if (0 == t.val)
                    return t.nullTxt || "必填";
                if (1 == t.val)
                    return "succ";
                var e = t.val.replace(/[^\x00-\xff]/g, "00");
                return t.min && e.length < t.min || t.max && e.length > t.max ? t.regTxt : t.regFlag && t.reg.test(t.val) ? t.regTxt : t.regFlag || !t.reg || t.reg.test(t.val) ? "succ" : t.regTxt
            }
              , r = function(t) {
                return 1 == t.val || 0 == t.val ? "succ" : t.nullTxt || "必填"
            }
              , a = {
                isNull: function(t) {
                    var r = {
                        val: t.val,
                        name: t.txt || e.isNull,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                nameLen: function(t) {
                    var r = {
                        val: t.val,
                        max: t.max || 40,
                        min: t.min || 2,
                        regTxt: t.txt || e.errorLength,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                name: function(t) {
                    var r = {
                        val: t.val,
                        max: t.max || 40,
                        min: t.min || 2,
                        reg: /[`~!@#\$%\^\&\*\(\)\+<>\?:"\{\},\.\\\/;'\[\]]/im,
                        regFlag: !0,
                        regTxt: t.txt || e.errorLetter,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                email: function(t) {
                    var r = {
                        val: t.val,
                        max: t.max || 48,
                        reg: /^([a-zA-Z0-9]+[_|\_|\.|\-]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.|\-]?)*[a-zA-Z0-9]+\.[a-zA-Z]{1,63}$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorEmail,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                url: function(t) {
                    var r = {
                        val: t.val,
                        reg: /(http|https):\/\/[^\s]+/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorUrl,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                num: function(t) {
                    var r = {
                        val: t.val,
                        reg: /\D/g,
                        max: t.max || 64,
                        min: t.min || 1,
                        regFlag: !0,
                        regTxt: t.txt || e.errorNum,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                money: function(t) {
                    var r = {
                        val: t.val,
                        reg: /^\d+(\.\d{1,2})?$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorMoney
                    };
                    return n(r)
                },
                pwd: function(t) {
                    var r = {
                        val: t.val,
                        reg: /^(?![0-9]+$)(?![a-z]+$)(?![A-Z]+$)(?![\-_]+$)[0-9A-Za-z]{6,18}$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorPwd,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                wechat: function(t) {
                    var r = {
                        val: t.val,
                        reg: /^[a-zA-Z0-9]{1}[a-zA-Z\d_\d-]{5,19}$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorWechat,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                qq: function(t) {
                    var r = {
                        val: t.val,
                        reg: /\D/g,
                        max: t.max || 12,
                        min: t.min || 6,
                        regFlag: !0,
                        regTxt: t.txt || e.errorQQ
                    };
                    return n(r)
                },
                industry: function(t) {
                    var r = {
                        val: t.val,
                        name: t.txt || e.isNull,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                innerOuterFlag: function(t) {
                    var n = {
                        val: t.val,
                        name: t.txt || e.isNull,
                        nullTxt: t.nullTxt
                    };
                    return r(n)
                },
                duty: function(t) {
                    var r = {
                        val: t.val,
                        name: t.txt || e.isNull,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                statement: function(t) {
                    var r = {
                        val: t.val,
                        name: t.txt || e.isNull,
                        nullTxt: t.nullTxt
                    };
                    return n(r)
                },
                companyname: function(t) {
                    var r = {
                        val: t.val,
                        max: t.max || 96,
                        reg: /^[a-zA-Z0-9_\-\u4E00-\u9FA5]+$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorCompany
                    };
                    return n(r)
                },
                cellphone: function(t) {
                    var e = {
                        val: t.val,
                        reg: /^((\d{3,4}-\d{7,14}))|(^1(3|4|5|6|7|8|9)\d{9})$/,
                        regFlag: !1,
                        regTxt: t.txt || "号码有误"
                    };
                    return n(e)
                },
                imageVerifyCode: function(t) {
                    var e = {
                        val: t.val,
                        reg: /^[0-9a-zA-Z]*$/g,
                        regFlag: !1,
                        regTxt: t.txt || "验证码有误"
                    };
                    return n(e)
                },
                username: function(t) {
                    var r = {
                        val: t.val,
                        max: t.max || 32,
                        reg: /^[a-zA-Z0-9_\-\u4E00-\u9FA5]+$/,
                        regFlag: !1,
                        regTxt: t.txt || e.errorUsername
                    };
                    return n(r)
                }
            };
            t.formJudge = function(t) {
                var e = []
                  , n = {};
                for (var r in t) {
                    var u = t[r]
                      , o = a[t[r].key](u)
                      , i = !1;
                    "succ" != o && (e.push(o),
                    i = !0,
                    n[r] = {
                        status: i,
                        txt: o
                    })
                }
                if (e.length > 0) {
                    delete n.succ;
                    for (var s in n)
                        if ("succ" != n[s].txt && (n[s].status = !0),
                        "true" == n[s].status) {
                            document.getElementById(s).focus();
                            var l = document.getElementById(s).offsetTop;
                            document.documentElement.scrollTop = l - 70;
                            break
                        }
                } else
                    n = {
                        succ: !0
                    };
                return n
            }
        }(window)
    },
    uBex: function(t, e) {},
    uuti: function(t, e, n) {
        "use strict";
        Date.getFirstDay = function(t) {
            return new Date(t.getFullYear(),t.getMonth(),1)
        }
        ,
        Date.isSameDay = function(t, e) {
            return t && e && t.getFullYear() === e.getFullYear() && t.getMonth() === e.getMonth() && t.getDate() === e.getDate()
        }
        ,
        Date.prototype.isSameDay = function(t) {
            return Date.isSameDay(this, t)
        }
        ,
        Date.prototype.Format = function(t) {
            t || (t = "yyyy-MM-dd");
            var e = {
                "M+": this.getMonth() + 1,
                "d+": this.getDate(),
                "h+": this.getHours(),
                "m+": this.getMinutes(),
                "s+": this.getSeconds(),
                "q+": Math.floor((this.getMonth() + 3) / 3),
                S: this.getMilliseconds()
            };
            /(y+)/.test(t) && (t = t.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length)));
            for (var n in e)
                new RegExp("(" + n + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? e[n] : ("00" + e[n]).substr(("" + e[n]).length)));
            return t
        }
    }
}, [0]);
//# sourceMappingURL=common-e0f006c9deb75fedd4a5.js.map
