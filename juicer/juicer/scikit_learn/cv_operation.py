# -*- coding: utf-8 -*-
from textwrap import dedent
from juicer.operation import Operation
from juicer.operation import ReportOperation
from juicer.scikit_learn.util import get_X_train_data
from juicer.scikit_learn.model_operation import AlgorithmOperation
from gettext import gettext

def get_caipirinha_config(config, indentation=0):
    limonero_conf = config['juicer']['services']['limonero']
    caipirinha_conf = config['juicer']['services']['caipirinha']
    result = dedent("""
    # Basic information to connect to other services
    config = {{
        'juicer': {{
            'services': {{
                'limonero': {{
                    'url': '{limonero_url}',
                    'auth_token': '{limonero_token}'
                }},
                'caipirinha': {{
                    'url': '{caipirinha_url}',
                    'auth_token': '{caipirinha_token}',
                    'storage_id': {storage_id}
                }},
            }}
        }}
    }}""".format(
        limonero_url=limonero_conf['url'],
        limonero_token=limonero_conf['auth_token'],
        caipirinha_url=caipirinha_conf['url'],
        caipirinha_token=caipirinha_conf['auth_token'],
        storage_id=caipirinha_conf['storage_id'], )
    )
    if indentation:
        return '\n'.join(
            ['{}{}'.format(' ' * indentation, r) for r in result.split('\n')])
    else:
        return result


class ReadImageFolderOperation(Operation):
    """
    Read Image Folder.
    Parameters: 
    """

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.folder_column = parameters.get('folder_column', 'None')
        self.image_column = parameters.get('image_column', 'None')

        self.has_code = len(named_inputs) >= 1 and any(
            [len(self.named_outputs) >= 1, self.contains_results()])
        self.output = self.named_outputs.get(
            'output data', 'output_data_{}'.format(self.order))

    def generate_code(self):
        if self.has_code:
            code = """
            storage_folder = "/srv/storage/srv/storage/limonero/data/"
            file_ext = ["**/*.jpg", "**/*.png"]

            folder_names = {inp}['{folder_column}']

            import glob
            
            folder_paths = []

            for name in folder_names:
                for ext in file_ext:
                    folder_paths.append(storage_folder+name+ext)            

            images = []
            for folder in folder_paths:
                images.extend(glob.glob(folder, recursive=True))

            df = pd.DataFrame(images, columns =['{image_column}'])

            {outp} = df
            
            #MPCE
            """ \
                .format(outp=self.output, inp=self.named_inputs['input data'],
                        folder_column=self.folder_column, image_column=self.image_column)
            return dedent(code)

class ExtractFacesOperation(Operation):
    """
    Extract Faces from images.
    Parameters: 
    """

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.image_prefix = parameters.get('image_prefix', 'face')
        self.image_column = parameters.get('image_column', 'None')
        self.face_column = parameters.get('face_column', 'None')
        self.face_location_column = parameters.get('face_location_column', 'None')
        self.normalize = parameters.get('normalize', '0')

        self.has_code = len(named_inputs) >= 1 and any(
            [len(self.named_outputs) >= 1, self.contains_results()])
        self.output = self.named_outputs.get(
            'output data', 'output_data_{}'.format(self.order))

    def generate_code(self):
        if self.has_code:
            code = """
            import face_recognition
            import dlib
            import os
            import cv2
            from imutils.face_utils import FaceAligner
            from PIL import Image

            storage_folder = "/srv/storage/srv/storage/limonero/data/"

            image_files = {inp}['{image_column}']

            df = pd.DataFrame([], columns=["{image_column}", "{face_column}", "{face_location_column}"])
            
            for image in image_files:
                try:
                    loaded_image = face_recognition.load_image_file(image)
                    face_locations = face_recognition.face_locations(loaded_image)

                    loaded_image_path = os.path.splitext(image)[0]
                    if "_{image_prefix}_" in loaded_image_path:
                            continue

                    predictor = dlib.shape_predictor("/usr/local/juicer/cv_data/shape_predictor_68_face_landmarks.dat")
                    fa = FaceAligner(predictor, desiredFaceWidth=256)

                    for index, face in enumerate(face_locations):
                        face_image_path = loaded_image_path + "_{image_prefix}_" + str(index) + ".jpg"
                        (top, right, bottom, left) = face
                                            
                        normalize = {normalize}
                        if normalize:
                            rec = dlib.rectangle(top=top, right=right, bottom=bottom, left=left)

                            rgb = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2RGB)
                            gray = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)

                            faceAligned = fa.align(loaded_image, gray, rec)                    
                            cropped_image = faceAligned
                            #cropped_image = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2RGB)
                        else:
                            cropped_image = loaded_image[top:bottom, left:right]
                        
                        im = Image.fromarray(cropped_image)
                        im.save(face_image_path)
                        df = pd.DataFrame([[image, face_image_path, face]], columns=["{image_column}", "{face_column}", "{face_location_column}"]).append(df, ignore_index=True)
                except Exception:
                    print("corrupted image")

            {outp} = df
            
            #MPCE
            """ \
                .format(outp=self.output, inp=self.named_inputs['input data'],
                        image_prefix=self.image_prefix, image_column=self.image_column, face_column=self.face_column, face_location_column=self.face_location_column, normalize=self.normalize)
            return dedent(code)

class ExtractFaceFeaturesOperation(Operation):
    """
    Extract Face Features from images.
    Parameters: 
    """

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.feature_column = parameters.get('feature_column', 'face')
        self.image_column = parameters.get('image_column', 'None')

        self.has_code = len(named_inputs) >= 1 and any(
            [len(self.named_outputs) >= 1, self.contains_results()])
        self.output = self.named_outputs.get(
            'output data', 'output_data_{}'.format(self.order))

    def generate_code(self):
        if self.has_code:
            code = """
            import face_recognition
            
            df = {inp}

            face_image_files = df['{image_column}']
            
            encodings = []

            for index, face_image in enumerate(face_image_files):
                loaded_image = face_recognition.load_image_file(face_image)
               
                face_encodinds = face_recognition.face_encodings(loaded_image)

                if len(face_encodinds) > 0:
                    encoding = face_encodinds[0]
                else:
                    encoding = np.zeros(128)
                
                encodings.append(encoding)
            
            df['{feature_column}'] = encodings

            {outp} = df
            
            #MPCE
            """ \
                .format(outp=self.output, inp=self.named_inputs['input data'],
                        feature_column=self.feature_column, image_column=self.image_column)
            return dedent(code)

class ChineseWhispersOperation(Operation):
    """
    Chinese Whispers Clustering.
    Parameters: 
    """

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.threshold = parameters.get('threshold', 'None')
        self.prediction = parameters.get('prediction', 'None')
        self.descriptors = parameters.get('descriptors', 'None')
        self.input = self.named_inputs['input data']
        self.has_code = len(named_inputs) >= 1 and any(
            [len(self.named_outputs) >= 1, self.contains_results()])
        self.output = self.named_outputs.get(
            'output data', 'output_data_{}'.format(self.order))
        self.transpiler_utils.add_import(
                    'import dlib')
        self.transpiler_utils.add_import(
                    'import pandas as pd')
        self.transpiler_utils.add_import(
                    'import numpy as np')

    def generate_code(self):
        if self.has_code:
            code = """
            {outp} = {inp}
            encodings = {outp}["{descriptors}"]
            encodings_vectors = []
            for encoding in encodings:
                encodings_vectors.append(dlib.vector(encoding.tolist()))
            labels = dlib.chinese_whispers_clustering(encodings_vectors, {threshold})
            {outp}["{prediction}"] = labels
            #MPCE
            """ \
                .format(outp=self.output, inp=self.input,
                        descriptors=self.descriptors, prediction=self.prediction, threshold=self.threshold)
            return dedent(code)

class ImageViewOperation(Operation):
    """
    Imae View Operation.
    Parameters: 
    """

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.image_column = parameters.get('image_column', 'MPCE')
        self.label_column = parameters.get('label_column', 'MPCE')

        #self.has_code = len(named_inputs) >= 1 and any(
        #    [len(self.named_outputs) >= 1, self.contains_results()])
        self.has_code = True
        self.title = "Teste"
        self.input = self.named_inputs['input data']
        self.output = self.named_outputs.get('visualization',
                                             'vis_task_{}'.format(self.order))

    def generate_code(self):
        if self.has_code:
            code = [dedent(get_caipirinha_config(self.config)),
            dedent("""

            #MPCE
            import face_recognition
            import math
            import imutils

            image_list = {inp}['{image_column}']
            label_list = {inp}['{label_column}']
            total_images = len(image_list)
            ncols = min(int(5), total_images)
            nrows = int(math.ceil(len(image_list)/ncols))
            thumb_size = 1.5

            import matplotlib.pyplot as plt
            from mpl_toolkits.axes_grid1 import ImageGrid
            import numpy as np
            import base64
            from io import BytesIO

            from juicer.service import caipirinha_service
            from juicer.scikit_learn.cv_operation import ImageVisualizationModel

            imgs = []

            for index, img in enumerate(image_list.tolist()):
                imgs.append({{'title': label_list.tolist()[index], 'src': img}})

            {outp} = ImageVisualizationModel(type_name='HTML', type_id=9000, task_id='{task_id}', title='{title}', data={{
                        'html': '',
                        'image_list': imgs
                    }})

            visualization = {{
                    'job_id': '{job_id}',
                    'task_id': {outp}.task_id,
                    'title': {outp}.title,
                    'type': {{
                        'id': {outp}.type_id,
                        'name': {outp}.type_name
                    }},
                    'model': {outp},
                    'data': json.dumps({outp}.data),
                }}
            

            #emit_event(
            #                'update task', status='COMPLETED',
            #                identifier='{task_id}',
            #                message='testando <b>html</b> agora',
            #                type='HTML', title='{title}',
            #                task={{'id': '{task_id}'}},
            #                operation={{'id': {operation_id}}},
            #                operation_id={operation_id})

            caipirinha_service.new_visualization(
                            config,
                            {user},
                            {workflow_id}, {job_id}, '{task_id}',
                            visualization, emit_event)
            """ \
                .format(outp=self.output, inp=self.input, image_column=self.image_column, label_column=self.label_column, task_id=self.parameters['task_id'], title=self.title, operation_id=self.parameters['operation_id'], job_id=self.parameters['job_id'], user=self.parameters['user'], workflow_id=self.parameters['workflow_id']))]
            
            return ''.join(code)

class ImgVisualizationModel(object):
    def __init__(self, data, task_id, type_id, type_name, title, column_names,
                 orientation,
                 id_attribute, value_attribute, params):
        self.data = data
        self.task_id = task_id
        self.type_id = type_id
        self.type_name = type_name
        self.title = title
        self.column_names = column_names
        self.orientation = orientation
        self.params = params
        self.default_time_format = '%Y-%m-%d'

        if len(id_attribute) > 0 and isinstance(id_attribute, list):
            self.id_attribute = id_attribute[0]
        else:
            self.id_attribute = id_attribute

        self.value_attribute = value_attribute

    def get_data(self):
        raise NotImplementedError(_('Should be implemented in derived classes'))

    def get_schema(self):
        return self.data.schema.json()

    def get_icon(self):
        return 'fa-question-o'

    def get_column_names(self):
        return ""
        
class ImageVisualizationModel(ImgVisualizationModel):
    
    def __init__(self, data=None, task_id=None, type_id=1, type_name=None,
                 title=None,
                 column_names=None,
                 orientation=None, id_attribute=None,
                 value_attribute=None, params=None):
        type_id = 9000
        type_name = 'html'
        if id_attribute is None:
            id_attribute = []
        if value_attribute is None:
            value_attribute = []
        if column_names is None:
            column_names = []
        ImgVisualizationModel.__init__(self, data, task_id, type_id, type_name,
                                    title, column_names, orientation,
                                    id_attribute, value_attribute, params)

    def get_icon(self):
        return "fa-html5"

    def get_data(self):
        return self.data

    def get_schema(self):
        return ''