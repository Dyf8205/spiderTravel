import {cF as lt, cG as it, r as i, d as pt, e, cH as B, s as mt, bi as ft, a5 as gt, f as c, cI as ht, bE as vt, bz as Pt, cJ as _t, cK as wt, cL as yt, cM as Et, cN as bt} from "./PVMBm82u.js";
import {m as S} from "./CUY6QCJb.js";
function Ct(a, r, d) {
    return a && a.length ? (r = r === void 0 ? 1 : lt(r),
    it(a, 0, r < 0 ? 0 : r)) : []
}
async function Lt(a) {
    return (await i("/api/_nuxt/cpath/fetch-product-comment-photos", {
        query: {
            ...a
        }
    }))?.data
}
async function Rt(a) {
    return await i("/api/_nuxt/cpath/fetch-product-comment-images", {
        method: "GET",
        query: a
    })
}
async function kt(a) {
    return await i("/api/_nuxt/cpath/fetch-product-comment-summary", {
        method: "GET",
        query: a
    })
}
async function Bt(a) {
    const {signal: r, ...d} = a;
    return await i("/api/_nuxt/cpath/fetch-product-comments-v2", {
        method: "GET",
        query: d,
        signal: r
    })
}
async function St(a) {
    return await i("/api/_nuxt/product/comment/helpful", {
        method: "POST",
        body: a
    })
}
async function xt(a) {
    return await i("/api/_nuxt/product/comment/translate", {
        method: "GET",
        query: a
    })
}
const Tt = {
    send: async a => {
        console.error("請改用 Nuxt 中的 request()")
    }
}
  , x = "KHSR"
  , Mt = pt("mobile-product", () => {
    const a = e(B.DEFAULT)
      , r = e({})
      , d = e(!1)
      , M = e(!1)
      , f = e(!1)
      , l = e(null)
      , u = e(null)
      , A = e({})
      , _ = e(null)
      , m = e(null)
      , g = e({
        current: 0,
        imageList: [],
        mediaList: [],
        videoList: []
    })
      , w = e([])
      , q = e(null)
      , y = e({})
      , U = e([])
      , F = e([])
      , G = e([])
      , K = e(null)
      , V = e(!1)
      , E = e({})
      , N = e({})
      , b = e("")
      , h = e({
        relatedData: !1,
        packageData: !1
    })
      , v = e([])
      , C = e(0)
      , P = e(!1)
      , L = e(!1)
      , T = e([])
      , H = e([])
      , I = e(null)
      , D = e(null)
      , R = e({
        isShow: !1,
        topicTag: ""
    })
      , {member: O} = mt(ft())
      , {getSiteUrl: j} = gt()
      , z = c( () => new ht(l.value))
      , k = c( () => u.value?.external_redirect_target !== x)
      , J = c( () => !!u.value?.is_marketplace)
      , W = c( () => u.value?.need_external_redirect && u.value?.external_redirect_target === x)
      , X = c( () => u.value?.destinations)
      , $ = c( () => P.value)
      , Q = c( () => L.value)
      , Y = c( () => T.value)
      , Z = c( () => I.value?.urlMapping?.reduce( (t, o) => (t[o?.productCategory] = o,
    t), {}) || {})
      , tt = c( () => m.value?.prod_mid ? vt(O.value?.wishProdIdList, m.value.prod_mid) : !1);
    function et(t) {
        a.value = t?.product.vertical ?? B.DEFAULT,
        l.value = t?.product,
        u.value = t?.product.prodInfo,
        m.value = t?.product.prodSetting,
        D.value = t?.constants,
        y.value = t?.recommend,
        r.value = t?.pointBonusBannerData,
        _.value = t?.product.descModules ?? {},
        R.value = t?.freshchat ?? {
            isShow: !1,
            topicTag: ""
        },
        P.value = t?.isBundleActive ?? !1;
        const o = S(Ct(t.product.prodInfo.covers.videos), p => ({
            type: "video",
            source_content: p.content
        }))
          , s = S(t.product.banner.list, p => ({
            type: "image",
            url: p.content,
            ccl: p.ccl,
            alt: p.alt || t.product.prodInfo.name
        }))
          , n = [...o, ...s];
        g.value = Pt(g.value, {
            imageList: s,
            mediaList: n,
            videoList: o
        })
    }
    async function ot({prodMid: t, page: o, travellerType: s}) {
        f.value = !0,
        d.value = !0;
        try {
            const {data: n} = await Lt({
                prodId: t,
                page: o,
                sort: s
            });
            if (n.result !== "0000")
                throw new Error(n);
            o === 0 ? v.value = n.photoList : v.value.push(...n.photoList),
            C.value = n.totalCount
        } catch (n) {
            console.error(n)
        } finally {
            d.value = !1,
            f.value = !1
        }
    }
    async function at({prodMid: t}) {
        if (k.value)
            try {
                const o = await _t(t)
                  , {data: s, error: n} = o;
                if (n)
                    throw new Error("get product related data error");
                w.value = s.data ?? []
            } catch (o) {
                console.error(o)
            } finally {
                h.value = {
                    ...h.value,
                    relatedData: !0
                }
            }
    }
    async function nt(t) {
        await Promise.allSettled([ct(t.prodSetting.prod_mid), st(t.prodSetting.prod_mid), rt(t.prodSetting.prod_oid)])
    }
    async function rt(t) {
        const {data: o} = await wt(t);
        b.value = o?.data?.data?.content || ""
    }
    async function st(t) {
        try {
            if (!t)
                throw new Error("prodMid is required");
            const {data: o} = await yt([t]);
            E.value = o?.data?.milesInfo || {}
        } catch (o) {
            console.error(o)
        }
    }
    async function ct(t) {
        try {
            if (!t)
                throw new Error("prodMid is required");
            const {data: o} = await Et(t);
            if (l.value && o) {
                const {prodSetting: s, productStatusMessage: n} = o.data;
                l.value.prodSetting = s,
                n && (l.value.productStatusMessage = n)
            }
        } catch (o) {
            console.error(o)
        }
    }
    function ut({payload: t}) {
        return new Promise( (o, s) => {
            Tt.send({
                url: j("product/ajax_get_bundle_package_detail"),
                method: "POST",
                data: {
                    bundle_pkg_oid: t.bundle_pkg_oid,
                    data: t.data
                }
            }).then(n => {
                o(n.data)
            }
            ).catch(n => {
                s(n)
            }
            )
        }
        )
    }
    async function dt(t) {
        const {data: o} = await bt({
            productOid: t
        });
        r.value = o?.data || {}
    }
    return {
        vertical: a,
        isFetching: d,
        loadingPageContent: M,
        isLoadPassengerPhoto: f,
        product: l,
        prodInfo: u,
        prodLocation: A,
        descModules: _,
        productSetting: m,
        banner: g,
        recommendProducts: w,
        guideLangs: q,
        recommend: y,
        breadCrumbs: U,
        breadCrumbTags: F,
        productMarketingConfig: G,
        reloadPageSecond: K,
        isNeedRemoveUrlUd1: V,
        milesPartnerInfo: E,
        pointBonusBannerData: r,
        merchantData: N,
        productAnnouncement: b,
        pageLoadingStatus: h,
        productCommentsPhotos: v,
        productCommentsPhotosTotalCount: C,
        isBundleActive: P,
        isFetchedBundlePkgs: L,
        bundlePkgs: T,
        bannerList: H,
        categoryConfig: I,
        constants: D,
        freshchat: R,
        productEventProperties: z,
        isProductRelatedDataRequired: k,
        isMarketplace: J,
        isExternalRedirect: W,
        destinations: X,
        getIsBundleActive: $,
        getIsFetchedBundlePkgs: Q,
        getBundlePkgs: Y,
        categoryUrlMapping: Z,
        isWishProduct: tt,
        fetchClientInitialData: nt,
        initState: et,
        getProductCommentPhotos: ot,
        getProductRelatedData: at,
        getBundlePackageDetail: ut,
        getPointBonusBannerData: dt
    }
}
);
export {Tt as K, kt as a, Rt as b, xt as c, Bt as f, St as p, Ct as t, Mt as u};
