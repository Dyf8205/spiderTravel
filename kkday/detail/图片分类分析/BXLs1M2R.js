import {b as R} from "./CSij-3UE.js";
import {f as o, e as n, w as A, df as f} from "./PVMBm82u.js";
function C(m) {
    const {prodId: l} = m
      , d = o( () => !!l && l.trim() !== "")
      , s = n(null)
      , r = n(1)
      , a = n([])
      , t = n(null)
      , c = n(!1)
      , i = n("")
      , g = o( () => t.value ? a.value.length >= t.value.pagination.total || r.value >= t.value.pagination.totalPages : !1)
      , u = async () => {
        if (d.value) {
            c.value = !0,
            i.value = "";
            try {
                const e = await R({
                    prodId: l,
                    page: r.value,
                    ...s.value !== null && {
                        type: s.value
                    }
                });
                if (e?.data?.data) {
                    const v = e.data.data;
                    a.value = [...a.value, ...v.images],
                    t.value = {
                        ...v.meta
                    }
                }
            } catch (e) {
                i.value = e instanceof Error ? e.message : "Failed to fetch comment images"
            } finally {
                c.value = !1
            }
        }
    }
      , P = async () => {
        await u()
    }
    ;
    function T() {
        g.value || (r.value++,
        u())
    }
    function p(e) {
        r.value = e,
        a.value = [],
        u()
    }
    function y(e) {
        s.value = e,
        r.value = 1,
        a.value = [],
        t.value = null,
        u()
    }
    A( () => l, () => {
        l && u()
    }
    , {
        immediate: !0
    });
    const O = o( () => a.value)
      , _ = o( () => t.value)
      , h = o( () => s.value);
    return {
        images: O,
        meta: _,
        loading: f(c),
        error: f(i),
        nextPage: T,
        selectPage: p,
        currentTravellerType: h,
        updateTravellerType: y,
        refresh: P
    }
}
const N = "PassengerPhoto"
  , w = "OfficialPhoto";
export {w as P, N as a, C as u};
