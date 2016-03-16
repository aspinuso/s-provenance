var meta = [
       {"term": "--Metadata--"},
       {"term":"_event_id"},
       {"term":"calib" },
       {"term":"channel"},
       {"term":" delta"},
       {"term":"depth_in_km"}, 
       {"term":"description"}, 
       {"term":"endtime"}, 
       {"term":"latitude"}, 
       {"term":"location"}, 
       {"term":"longitude"}, 
       {"term":"m_pp"}, 
       {"term":"m_rp"}, 
       {"term":"m_rr"}, 
       {"term":"m_rt"}, 
       {"term":"m_tp"}, 
       {"term":"m_tt"}, 
       {"term":"magnitude"},
       {"term":"mime-type"},
       {"term":"network"}, 
       {"term":"npts"}, 
       {"term":"origin_time"},
       {"term":" path"}, 
       {"term":"sampling_rate"},
       {"term":" starttime"}, 
       {"term":"station"}, 
       {"term":"type"},
       {"term": "--Parameters--"},
       {"term": "ABSORB_INSTEAD_OF_FREE_SURFACE"},
       {"term": "ANISOTROPY"},
       {"term": "ATTENUATION"},
       {"term": "CREATE_SHAKEMAP"}, 
       {"term": "DT"},
       {"term": "f0_FOR_PML"},
       {"term": "GPU_MODE"},
       {"term": "GRAVITY"},
       {"term": "HDUR_MOVIE"}, 
       {"term": "LOCAL_PATH"},
       {"term": "MODEL"},
       {"term": "MOVIE_SURFACE"},
       {"term": "MOVIE_TYPE"},
       {"term": "MOVIE_VOLUME"},
       {"term": "NGNOD"},
       {"term": "NOISE_TOMOGRAPHY"},
       {"term": "NPROC"},
       {"term": "NTSTEP_BETWEEN_FRAMES"},
       {"term": "NTSTEP_BETWEEN_OUTPUT_INFO"}, 
       {"term": "NTSTEP_BETWEEN_OUTPUT_SEISMOS"}, 
       {"term": "NTSTEP_BETWEEN_READ_ADJSRC"}, 
       {"term": "OLSEN_ATTENUATION_RATIO"}, 
       {"term": "PML_CONDITIONS"}, 
       {"term": "PML_INSTEAD_OF_FREE_SURFACE"}, 
       {"term": "PML_WIDTH_MAX"}, 
       {"term": "PML_WIDTH_MIN"}, 
       {"term": "PRINT_SOURCE_TIME_FUNCTION"}, 
       {"term": "ROTATE_PML_ACTIVATE"}, 
       {"term": "ROTATE_PML_ANGLE"}, 
       {"term": "SAVE_DISPLACEMENT"}, 
       {"term": "SAVE_FORWARD"}, 
       {"term": "SAVE_MESH_FILES"}, 
       {"term": "OCEANS"}, 
       {"term": "NSTEP"}, 
       {"term": "SIMULATION_TYPE"},
       {"term": "SUPPRESS_UTM_PROJECTION"},
       {"term": "TOMOGRAPHY_PATH"},
       {"term": "TOPOGRAPHY"},
       {"term": "USE_FORCE_POINT_SOURCE"}, 
       {"term": "USE_HIGHRES_FOR_MOVIES"}, 
       {"term": "USE_OLSEN_ATTENUATION"}, 
       {"term": "USE_RICKER_TIME_FUNCTION"}, 
       {"term": "UTM_PROJECTION_ZONE"}
       ];

Ext.define('CF.store.SeismoMeta', {
  extend: 'Ext.data.Store',
  model: 'CF.model.SeismoMeta',
  data: meta
});