export const addCommonMocks = (maxios) => {
  maxios.onGet('/carousel/images/').reply(
    200, {
      status: 'success',
      message: 'And now for something completely different.',
      images: [],
    })
}


