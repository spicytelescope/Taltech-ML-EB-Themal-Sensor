/*
 * app_x_cube_ai_temporary.c
 *
 *  Created on: 3. nov 2020
 *      Author: Mairo Leier
 */

static ai_buffer ai_input[AI_NETWORK_IN_NUM] = AI_NETWORK_IN ;
static ai_buffer ai_output[AI_NETWORK_OUT_NUM] = AI_NETWORK_OUT ;

// TODO: LAB8: Move all the following functions to the automatically generated app_x-cube-ai.c file.
// As MX_X_CUBE_AI_Process_2() function will be executed in the main loop, you need to add its prototype to the header file.
int aiInit(const ai_u8* activations) {
    ai_error err;

    /* 1 - Specific AI data structure to provide the references of the
     * activation/working memory chunk and the weights/bias parameters */
    const ai_network_params params = {
            AI_NETWORK_DATA_WEIGHTS(ai_network_data_weights_get()),
            AI_NETWORK_DATA_ACTIVATIONS(activations)
    };

    /* 2 - Create an instance of the NN */
    err = ai_network_create(&network, AI_NETWORK_DATA_CONFIG);
    if (err.type != AI_ERROR_NONE) {
	    return -1;
    }

    /* 3 - Initialize the NN - Ready to be used */
    if (!ai_network_init(network, &params)) {
        err = ai_network_get_error(network);
        if(err.type !=AI_ERROR_NONE){
        	printf("ERROR : type=%d code=%d\r\n",err.type,err.code);
        }
        ai_network_destroy(network);
        network = AI_HANDLE_NULL;
	    return -2;
    }

    return 0;
}

/*
 * Run function to execute an inference.
 */
int aiRun(const void *in_data, void *out_data) {
    ai_error err;

    /* Initialize input/output buffer handlers */
    ai_input[0].n_batches = 1;
    ai_input[0].data = AI_HANDLE_PTR(in_data);
    ai_output[0].n_batches = 1;
    ai_output[0].data = AI_HANDLE_PTR(out_data);

    /* 2 - Perform the inference */
     ai_network_run(network, &ai_input[0], &ai_output[0]);
     err = ai_network_get_error(network);
    printf("ERROR : type=%d code=%d\r\n",err.type,err.code);

}

// Process NN input data and output predictions
void MX_X_CUBE_AI_Process_2(ai_float * nn_input_data, ai_float *nn_output_data) {
     aiRun(nn_input_data, nn_output_data);
}
