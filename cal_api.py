from os import times
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

from xml_extractor import scrap_pages

import requests, time

def calorie_info(image_path):
    neutrition_data = {
        'Bread': [966,11.2,2.3,37.7,2.7,421,0.29,33],
        'Egg' : [574,12.4,9.5,0.7,0.3,127,0.6,67],
        'Tomato' : [77.8,0.6,0,3,0.5,4,0.53,128],
        'Macroon' : [260,11.2,45,165,0.415,18],
        'Sausage' : [909,17.2,14.9,3.8,0.4,795,0.62,143]

    }
    res = {}
    safe_res = {}
    with open(image_path, "rb") as image_file:
        image_f = image_file.read()

    # print(image_f)

    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

    # This is how you authenticate.
    metadata = (('authorization', 'Key c7bb08b132e347e8b255ec1da9643270'),)

    request = service_pb2.PostModelOutputsRequest(
        # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
        model_id='bd367be194cf45149e75f01d59f77ba7',
        inputs=[
        resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_f
                        )
                    )
                )
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        return 'No_food'
    myWolframAppId = 'VW4AAW-43H9PK84A4'
    print(response)
    value = []
    detections = {}
    for concept in response.outputs[0].data.concepts:
        
        print('%12s: %.2f' % (concept.name, concept.value))
        if concept.value * 100 > 89.0:
            
           
            const = ''
            for i in  range(len(concept.name.split(' '))):
                const += concept.name.split(' ')[i] + '%20'
                

            const = const[:-3]
            # print(const)
            
            # url = 'http://api.wolframalpha.com/v2/query?input='+const+'%20nutrition%20facts&appid='+myWolframAppId
            # print(url)
            value.append(concept.value)
            res[concept.name] = concept.value
            # time.sleep(2)
        detections[concept.name] = concept.value
    final = {}
    value_f = value[0]
    for key, vaue in res.items():
        diff = abs(value_f - vaue)
        print(diff)
        if diff > 0.05:
            break 
        value_f = vaue
        final[key] = vaue
        if str(key).lower() in [i.lower for i in neutrition_data.keys()]:
            print(neutrition_data)

    return final, detections

if __name__ == '__main__':
    print(calorie_info(r'images\Bread,_Tomato_and_Macroon_on_Plate.jpg'))