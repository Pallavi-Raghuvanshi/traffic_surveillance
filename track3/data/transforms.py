from torchvision import transforms

from track3.core.config import CONFIG


train_transform = transforms.Compose([

    transforms.Resize(CONFIG.input_size),

    transforms.RandomHorizontalFlip(),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=CONFIG.imagenet_mean,

        std=CONFIG.imagenet_std,

    ),

])


test_transform = transforms.Compose([

    transforms.Resize(CONFIG.input_size),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=CONFIG.imagenet_mean,

        std=CONFIG.imagenet_std,

    ),

])