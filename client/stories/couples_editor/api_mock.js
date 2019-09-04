import {addCommonMocks} from '../common_api_mock'
export const addMocks = (maxios) => {
  addCommonMocks(maxios)
  //maxios.onGet('/search/api/search').reply(200, api_results)
}


