
const arrayBufferToBase64 = (buffer) => {
  var binary = ''
  var bytes = [].slice.call(new Uint8Array(buffer));

  bytes.forEach((b) => binary += String.fromCharCode(b));

  return btoa(binary)
}

export const imageToUrl = (url) => {
    return fetch(url)
            .then(res => {
                return res.arrayBuffer()
            }).then(buffer => {

                const base64Flag = 'data:image/png;base64,'
                const imageString = arrayBufferToBase64(buffer)
                return base64Flag + imageString
            })
}
