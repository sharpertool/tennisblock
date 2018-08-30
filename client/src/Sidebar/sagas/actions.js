import map from 'lodash/map'
import reject from 'lodash/reject'
import reduce from 'lodash/reduce'
import axios from 'axios'

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'

export function fetchContents(tree) {

    const limit = 12 - 1
    //initial data at first load
    const urls = reduce(tree, (r, v, k) => {
        if(k <= limit) {
            r.push(v.url)
            if(v.children) {
                map(v.children, (cv, ck) => {
                    r.push(cv.url)
                    if(cv.children) {
                        map(cv.children, (_cv, _ck) => {
                            r.push(_cv.url)
                        })
                    }
                })
            }
        }
        return r
    }, [])


    const requests = urls.map((v, k) => {
        return axios.get(v)
    })

    return axios.all(requests).then((responses) => {
        return responses.map((v, k) => v.data.trim())
    })
}


export function fetchPrevContents(tree, first_child) {

    const index = reduce(tree, (r, v, k) => {
        if(v.slug == first_child) {
            r.push(k)
        }
        return r
    }, [])[0]


    const limit = index - 1

    const urls = reduce(tree, (r, v, k) => {
        if(k == limit) {
            r.push(v.url)
            if(v.children) {
                map(v.children, (_v, _k) => {
                    r.push(_v.url)
                    if(_v.children) {
                        map(_v.children, (_vc, _kc) => {
                            r.push(_vc.url)
                        })
                    }
                })
            }
        }
        return r
    }, [])

    const requests = urls.map((v, k) => {
        return axios.get(v)
    })

    return axios.all(requests).then((responses) => {
        console.log(responses)
        return responses.map((v, k) => v.data.trim())
    })
}

//Last work
export function fetchDirectContents(tree, slug) {
    const limit = 12 - 1
    const urls = reduce(tree, (r, v, k) => {
        if(k <= k + limit && v.slug == slug) {
            r.push(v.url)
            if(v.children) {
                map(v.children, (cv, ck) => {
                    r.push(cv.url)
                    if(cv.children) {
                        map(cv.children, (_cv, _ck) => {
                            r.push(_cv.url)
                        })
                    }
                })
            }
        }
        return r
    }, [])

    const requests = urls.map((v, k) => {
        return axios.get(v)
    })

    return axios.all(requests).then((responses) => {
        return responses.map((v, k) => v.data.trim())
    })
}


export function fetchNextContents(tree, last_child) {
    const index = reduce(tree, (r, v, k) => {
        if(v.slug == last_child) {
            r.push(k)
        } else if(v.children) {
            reduce(v.children, (rc, vc, kc) => {
                if(vc.slug == last_child) {
                    r.push(k)
                } else if(vc.children) {
                    reduce(vc.children, (rcc, vcc, kcc) => {
                        if(vcc.slug == last_child) {
                            r.push(k)
                        }
                    }, [])
                }
                return rc
            }, [])
        }
        return r
    }, [])[0] + 1
    const last_index = index + 2
    const urls = reduce(tree, (r, v, k) => {
        if(k >= index && k <= last_index) {
            r.push(v.url)
            if(v.children) {
                map(v.children, (cv, ck) => {
                    r.push(cv.url)
                    if(cv.children) {
                        map(cv.children, (_cv, _ck) => {
                            r.push(_cv.url)
                        })
                    }
                })
            }
        }
        return r
    }, [])

    const requests = urls.map((v, k) => {
        return axios.get(v)
    })

    return axios.all(requests).then((responses) => {
        return responses.map((v, k) => v.data.trim())
    })
}
