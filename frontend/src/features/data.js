import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import Cookies from 'js-cookie'

export const geojson = createAsyncThunk(
    'geojson',
    async (thunkAPI) => {
        try{
            const res = await fetch(
				`${process.env.REACT_APP_API_URL}api/main/geojson/`
			,{
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
            });
            const data = await res.json();
            if (res.status === 200) {
                return data;   
            } else {
                return thunkAPI.rejectWithValue(data);
            }

        } catch (err) {
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
)

export const raster = createAsyncThunk(
    'raster',
    async (thunkAPI) => {
        try{
            const res = await fetch(
				`${process.env.REACT_APP_API_URL}api/main/rasters/`
			,{
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
            });
            const data = await res.json();
            if (res.status === 200) {
                return data;   
            } else {
                return thunkAPI.rejectWithValue(data);
            }

        } catch (err) {
            
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
)

export const upload_geojson = createAsyncThunk(
    'geojson/upload',
    async ({geojson,user},thunkAPI) => {
        
          const body = JSON.stringify({
            geojson,
            user,
        });

        try{
            const res = await fetch(
				`${process.env.REACT_APP_API_URL}api/main/upload/`
			,{
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
                body,
            });
            

            const data = await res.json();

            if (res.status === 201) {

                return data;   
            } else {

                return thunkAPI.rejectWithValue(data);
            }

        } catch (err) {
            
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
);


export const upload_raster = createAsyncThunk(
    'rasters/upload',
    async ({raster,user},thunkAPI) => {
        
        const name = raster.name
        const body = JSON.stringify({
            raster,
            name,
            user
        });

        try{
            const res = await fetch(
				`${process.env.REACT_APP_API_URL}api/main/raster/`
			,{
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
                body,
            });

            const data = await res.json();

            if (res.status === 201) {
                return data;                
            } else {
                return thunkAPI.rejectWithValue(data);
            }

        } catch (err) {
            return thunkAPI.rejectWithValue(err.response.data);
        }
    }
)

export const delete_geojson = createAsyncThunk(
    'geojson/delete',
    async({id},thunkAPI) => {
        try {
            const res = await fetch(
                `${process.env.REACT_APP_API_URL}api/main/geojson/${id}`
			,{
                method: 'DELETE',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
            });

            if (res.ok) {
                return id;

              } else {
                const data = await res.json();
                return thunkAPI.rejectWithValue(data);
              }
            
        } catch (error) {
            return thunkAPI.rejectWithValue(error.response.data);
        }
    }
    )

export const delete_raster = createAsyncThunk(
    'raster/delete',
    async ({id},thunkAPI) => {
        try {
            const res = await fetch(
                `${process.env.REACT_APP_API_URL}api/main/rasters/${id}`
			,{
                method: 'DELETE',
                headers: {
                    Accept: 'application/json',
                    Authorization: `Bearer ${Cookies.get('access_token')}`
                },
            });

            if (res.ok) {
                return id;

              } else {
                const data = await res.json();
                return thunkAPI.rejectWithValue(data);
              }
            
        } catch (error) {
            return thunkAPI.rejectWithValue(error.response.data);
        }
    }
)

const initialState =  {
    geojson: [],
    vector: [],
    raster: [],
    loading: true,
}

const dataSlice = createSlice({
    name:'data',
    initialState,
    reducers:{
        addGeojsons:(state,action) => {
            state.geojson = action.payload;
        },
        addRasters:(state,action) => {
            state.raster = action.payload;
        }
        // resetRegistered: state => {
        //     state.registered = false
        // },
    },
    extraReducers: builder => {
        builder
            .addCase(geojson.pending, state => {
                state.loading = true;
            })
            .addCase(geojson.fulfilled, (state, action) => {
                state.loading = false;
                state.geojson = action.payload;
            })
            .addCase(geojson.rejected, state => {
                state.loading = false;
            })
            .addCase(raster.pending, state => {
                state.loading = true;
            })
            .addCase(raster.fulfilled, (state, action) => {
                state.loading = false;
                state.raster = action.payload;
            })
            .addCase(raster.rejected, state => {
                state.loading = false;
            })

    }
})

// export const { resetRegistered } = userSlice.actions;
export const {addGeojsons,addRasters} = dataSlice.actions;
export default dataSlice.reducer;