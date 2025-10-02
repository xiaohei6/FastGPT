import { Module, Controller, Get } from '@nestjs/common';
import { SandboxController } from './sandbox/sandbox.controller';
import { SandboxService } from './sandbox/sandbox.service';

@Controller()
class AppController {
  @Get()
  getRoot() {
    return {
      message: 'FastGPT Sandbox Service',
      version: '1.0.0',
      endpoints: {
        'GET /': 'This information',
        'GET /sandbox': 'Sandbox service info',
        'POST /sandbox/js': 'Execute JavaScript code',
        'POST /sandbox/python': 'Execute Python code',
        'GET /api': 'Swagger API documentation'
      }
    };
  }
}

@Module({
  imports: [],
  controllers: [AppController, SandboxController],
  providers: [SandboxService]
})
export class AppModule {}
